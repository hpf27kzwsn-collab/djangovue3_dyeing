"""报价查询与试算复用已有资料查询权限；采用走订单原POST/PATCH/整单保存。"""
from copy import copy
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from . import source_order_pricing as pricing
from .business_api import ActionInput
from core.responses import success


class PricingInput(serializers.Serializer):
    mode=serializers.ChoiceField(choices=['quote','manual'])
    quote_id=serializers.IntegerField(required=False)
    quote_head_id=serializers.IntegerField(required=False)
    yarn_category=serializers.ChoiceField(choices=list(pricing.YARNS),required=False)
    price_basis=serializers.ChoiceField(choices=['CusPrice','Price'],default='CusPrice')
    price_unit=serializers.ChoiceField(choices=list(pricing.UNITS),required=False,allow_null=True)
    quantity_mode=serializers.ChoiceField(choices=['order','explicit'],default='order')
    quantity=serializers.DecimalField(max_digits=20,decimal_places=6,required=False,allow_null=True)
    manual_price=serializers.DecimalField(max_digits=8,decimal_places=2,required=False,allow_null=True)
    amount_mode=serializers.ChoiceField(choices=['calculated','manual'],default='calculated')
    manual_amount=serializers.DecimalField(max_digits=10,decimal_places=2,required=False,allow_null=True)
    reason=serializers.CharField(required=False,allow_blank=True,default='',trim_whitespace=False)

    def to_internal_value(self,data):
        unknown=set(data)-set(self.fields)
        if unknown:raise serializers.ValidationError({k:'订单选价不接收此字段。' for k in unknown})
        # PATCH只部分修改订单；其中的选价命令仍是一条完整的新采用指令。
        if 'mode' not in data:raise serializers.ValidationError({'mode':'请选择报价或手工议价。'})
        return super().to_internal_value({'price_basis':'CusPrice','quantity_mode':'order','amount_mode':'calculated','reason':'',**data})


class PricingLineInput(serializers.Serializer):
    old_prod_id=serializers.CharField(required=False,allow_null=True,allow_blank=True,trim_whitespace=False,max_length=30)
    old_unit=serializers.CharField(required=False,allow_null=True,allow_blank=True,trim_whitespace=False,max_length=50)
    old_order_qty=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True,required=False)
    old_card_qty=serializers.IntegerField(required=False,allow_null=True)


class PricingQueryInput(ActionInput):
    order_id=serializers.IntegerField(required=False,allow_null=True)
    line_id=serializers.IntegerField(required=False,allow_null=True)
    sheet_series=serializers.CharField(required=False,allow_null=True,allow_blank=True,trim_whitespace=False)
    customer_id=serializers.CharField(required=False,allow_null=True,allow_blank=True,trim_whitespace=False)
    yarn_category=serializers.ChoiceField(choices=list(pricing.YARNS),required=False)
    line=PricingLineInput()
    pricing=PricingInput(required=False)


def query_values(view):
    s=PricingQueryInput(data=view.request.data,context={'request':view.request})
    s.is_valid(raise_exception=True)
    data=s.validated_data;read=pricing.reader(view.request.user)
    # 候选/试算仅需要现有订单及报价查询授权，不借新动作绕过来源范围。
    rows=read.source(pricing.model('OrderColor'),pricing.LINE_COLUMNS)
    if data.get('line_id'):
        item=copy(get_object_or_404(rows,pk=data['line_id']))
    else:item=pricing.model('OrderColor')()
    head_rows=read.source(pricing.model('OrderMain'),pricing.HEAD_COLUMNS)
    if data.get('order_id'):
        head=get_object_or_404(head_rows,pk=data['order_id'])
    elif data.get('sheet_series'):
        from .source_business_updates import matching
        heads=list(matching(head_rows,SheetSeries=data['sheet_series'])[:2])
        if len(heads)!=1:raise serializers.ValidationError({'order_id':'请明确选择所属订单表头。'})
        head=heads[0]
    else:head=pricing.head_for(item,view.request.user)
    head=copy(head)
    if 'customer_id' in data:head.old_customer_id=data['customer_id']
    for key,value in data['line'].items():setattr(item,key,value)
    return item,head,data


class OrderPricingMixin:
    @action(methods=['post'],detail=False,permission_classes=[IsAuthenticated])
    def pricing_candidates(self,request):
        item,head,data=query_values(self)
        if 'yarn_category' not in data:raise serializers.ValidationError({'yarn_category':'请选择供纱方式。'})
        return success({'rows':pricing.candidates(request.user,head.old_customer_id,item.old_prod_id,data['yarn_category']),
            'units':[{'value':k,'label':v} for k,v in pricing.UNITS.items()]})

    @action(methods=['post'],detail=False,permission_classes=[IsAuthenticated])
    def pricing_preview(self,request):
        item,head,data=query_values(self)
        if 'pricing' not in data:raise serializers.ValidationError({'pricing':'请选择本次计价方式。'})
        values,state=pricing.selection(item,data['pricing'],request.user,head=head)
        return success({'price':values['old_price'],'amount':values['old_amount'],'adoption':state})

    @action(methods=['get'],detail=True,permission_classes=[IsAuthenticated])
    def pricing_lines(self,request,pk=None):
        head=get_object_or_404(pricing.reader(request.user).source(pricing.model('OrderMain'),pricing.HEAD_COLUMNS),pk=pk)
        rows=pricing.lines_for(head,request.user)
        return success({'order_id':head.pk,'sheet_no':head.old_sheet_no,'customer_id':head.old_customer_id,
            'historical':pricing.is_historical(head),'summary':pricing.summary(head,request.user),
            'rows':[{'id':r.pk,**{k:getattr(r,k) for k in pricing.LINE_COLUMNS},'pricing_info':pricing.info(r)} for r in rows]})
