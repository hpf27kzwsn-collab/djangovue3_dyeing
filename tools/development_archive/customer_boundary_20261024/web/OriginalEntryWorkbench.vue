<script setup lang="ts">
import {computed,onMounted,ref} from 'vue'
import {useRouter} from 'vue-router'
import {api} from '../../api'
import OriginalLayoutReview from './OriginalLayoutReview.vue'
const props=defineProps<{entity:string}>(),router=useRouter()
const base=computed(()=>`/api/system/${props.entity}/`)
const catalog=ref<any[]>([]),selected=ref(''),detail=ref<any>(),result=ref<any>(),busy=ref(false)
const printing=ref<any>(),reportSearch=ref('')
const layout=ref<any>(),layoutVisible=ref(false)
const proof=ref<any>(),proofVisible=ref(false)
const printParent=ref<string|null>(null)
const printNull=ref(false)
async function createProof(index:number){
  proof.value=(await api(base.value+'phase6_template/',{method:'POST',data:{index,format:'Proof',parameters:params.value,print_key:printParent.value,print_null_key:printNull.value,load_records:loadRecords.value,include_retained:includeRetained.value}})).data
  proofVisible.value=true
}
async function previewLayout(index:number){layout.value=(await api(base.value+'phase6_template/',{method:'POST',data:{index,format:'Layout'}})).data;layoutVisible.value=true}
const templates=computed(()=>printing.value?.reports.filter((r:any)=>[r.RptID,r.RptTitle,r.data_member].some(v=>String(v??'').toLowerCase().includes(reportSearch.value.toLowerCase())))??[])
const params=ref<Record<string,any>>({}),loadRecords=ref(false),includeRetained=ref(true),calculateFormulas=ref(false),page=ref(1)
const viewRows=computed(()=>result.value?.rows.slice((page.value-1)*50,page.value*50)??[])
const display=(v:any)=>v===null?'〈NULL〉':typeof v==='object'?JSON.stringify(v):String(v)
onMounted(async()=>{const [a,b]=await Promise.all([api(base.value+'phase6_catalog/'),api(base.value+'phase6_catalog/',{params:{reports:1}})]);catalog.value=a.data;printing.value=b.data})
async function select(){detail.value=undefined;result.value=undefined;params.value={};printParent.value=null;printNull.value=false;detail.value=(await api(base.value+'phase6_catalog/',{params:{entry:selected.value}})).data;for(const name of detail.value.query_support.parameters??[])params.value[name]=null}
async function query(){busy.value=true;try{result.value=(await api(base.value+'phase6_query/',{method:'POST',data:{entry:selected.value,parameters:params.value,load_records:loadRecords.value,include_retained:includeRetained.value,calculate_formulas:calculateFormulas.value}})).data;page.value=1}finally{busy.value=false}}
function exportRows(){
  const quote=(v:any)=>'"'+(v===null?'\\N':String(v).replaceAll('\\','\\\\')).replaceAll('"','""')+'"'
  const text=[result.value.columns.map((c:any)=>quote(c.name)).join(','),...result.value.rows.map((row:any[])=>row.map(quote).join(','))].join('\r\n')
  const href=URL.createObjectURL(new Blob(['\ufeff'+text],{type:'text/csv;charset=utf-8'})),link=document.createElement('a');link.href=href;link.download=selected.value+'.csv';link.click();URL.revokeObjectURL(href)
}
async function downloadTemplate(index:number,format:string){
  const blob=await api(base.value+'phase6_template/',{method:'POST',data:{index,format},responseType:'blob'}) as unknown as Blob
  const href=URL.createObjectURL(blob),link=document.createElement('a');link.href=href;link.download=`原模板-${index}.${format==='TemplateXml'?'xml':'cs'}`;link.click();URL.revokeObjectURL(href)
}
const hooks=computed(()=>Object.entries(detail.value?.table??{}).filter(([key,value])=>/^(Before|After).*SQL$/.test(key)&&value))
</script>
<template>
  <div class="entry-workbench">
    <el-select v-model="selected" filterable placeholder="按旧入口名称或业务名称搜索（含异常及停用入口）" @change="select" style="width:100%">
      <el-option v-for="entry in catalog" :key="entry.name" :value="entry.name" :label="`${entry.title||entry.name} · ${entry.name}${entry.finance?' · 财务暂缓':''}`"/>
    </el-select>
    <template v-if="detail">
      <p>{{detail.table.Alias}} · {{detail.table.Kind}} · {{detail.fields.length}} 个原字段配置</p>
      <el-alert v-if="detail.finance" title="财务入口暂缓开发，原配置保留。" type="info" :closable="false"/>
      <el-alert v-else-if="detail.query_support.query_state==='unresolved'" title="此入口查询有待解决差异，下方保留原查询、字段及原表入口。" type="warning" :closable="false"/>
      <el-alert v-else-if="detail.query_support.query_state==='reconstructed_missing_projection'" title="此查询采用已注明的替代取数方案，未知字段保持 NULL；尚未等价复刻。" type="warning" :closable="false"/>
      <div v-if="detail.query_support.live_original"><p>旧库核验：{{detail.query_support.live_original.category}}。{{detail.query_support.live_original.historical_reconciliation}}</p><p v-for="(error,index) in detail.query_support.live_original.errors" :key="index">{{error.message}}</p></div>
      <div class="actions"><el-button v-for="model in detail.models" :key="model" @click="router.push({path:'/system/'+model.replace('.','_').toLowerCase(),query:{_entry:selected}})">打开对应原表 {{model.split('.')[1]}}</el-button></div>
      <p v-for="binding in detail.write_bindings.filter((b:any)=>b.reason)" :key="binding.model">本入口采用 {{binding.table}}：{{binding.reason}}</p>
      <el-tabs>
        <el-tab-pane label="原查询与数据">
          <p v-if="detail.query_support.parameter_note">{{detail.query_support.parameter_note}}</p>
          <el-form label-width="170px"><el-form-item v-for="(_,name) in params" :key="name" :label="detail.query_support.parameter_labels?.[name]??String(name)"><el-select v-if="detail.query_support.parameter_options?.[name]" v-model="params[name]" placeholder="选择本次查询的数量维度"><el-option v-for="option in detail.query_support.parameter_options[name]" :key="option.value" :value="option.value" :label="option.label"/></el-select><el-date-picker v-else-if="detail.query_support.parameter_types?.[name]==='date'" v-model="params[name]" value-format="YYYY-MM-DD"/><el-input v-else v-model="params[name]" clearable/><el-button @click="params[name]=null">设为空值</el-button></el-form-item></el-form>
          <el-checkbox v-model="loadRecords">加载记录（解除旧界面外层的空表初始化条件）</el-checkbox>
          <el-checkbox v-model="includeRetained">包含已撤回留档的原行</el-checkbox>
          <el-checkbox v-model="calculateFormulas">附加原公式试算列</el-checkbox>
          <el-button :loading="busy" :disabled="!['executed_empty_fixture','reconstructed_missing_projection'].includes(detail.query_support.query_state)" @click="query">查询</el-button>
          <template v-if="result">
            <p v-if="result.formula_note">{{result.formula_note}}</p>
            <el-collapse v-if="result.formula_source_resolutions?.length"><el-collapse-item title="原公式来源调整依据"><el-table :data="result.formula_source_resolutions"><el-table-column prop="field" label="原字段"/><el-table-column prop="original_expression" label="原表达式"/><el-table-column prop="basis" label="当前处理依据" min-width="320"/></el-table></el-collapse-item></el-collapse>
            <el-collapse v-if="result.formula_issues?.length"><el-collapse-item :title="'逐行公式差异（'+result.formula_issues.length+'）'"><el-table :data="result.formula_issues" height="240"><el-table-column prop="row" label="结果行号"/><el-table-column prop="field" label="原字段"/><el-table-column prop="reason" label="原因" min-width="320"/></el-table></el-collapse-item></el-collapse>
            <div v-if="result.reconstruction"><p>{{result.reconstruction.join_note}}</p><p v-for="column in result.reconstruction.missing_columns" :key="column.source">{{column.source}}：{{column.reason}}</p></div>
            <p>本次完整结果 {{result.count}} 行；每页 50 行。重复行、重名列保留；〈NULL〉表示未填写，空白表示空字符串。</p>
            <el-button @click="exportRows">导出本次全部结果 CSV</el-button>
            <el-table :data="viewRows" height="45vh" border><el-table-column v-for="(col,index) in result.columns" :key="col.key" :label="col.title+' ['+col.name+']'" min-width="160"><template #default="scope">{{display(scope.row[index])}}</template></el-table-column></el-table>
            <el-pagination v-model:current-page="page" :page-size="50" :total="result.count" layout="prev,pager,next,total"/>
          </template>
          <el-collapse><el-collapse-item title="原查询及差异依据"><pre>{{detail.table.SQL}}</pre><pre v-if="detail.query_support.error">{{detail.query_support.error}}</pre></el-collapse-item></el-collapse>
        </el-tab-pane>
        <el-tab-pane label="原字段设置">
          <el-table :data="detail.fields" height="60vh" border><el-table-column prop="FieldName" label="原字段" width="200"/><el-table-column prop="FieldCaption" label="原标题" width="160"/><el-table-column prop="FieldKind" label="生成方式" width="180"/><el-table-column prop="IsReadOnly" label="原只读"/><el-table-column prop="IsRequired" label="原必填"/><el-table-column prop="DefaultValue" label="默认值"/><el-table-column prop="DisplayFormat" label="展示格式"/><el-table-column prop="Express" label="原计算表达式" min-width="300"/><el-table-column prop="GenerateTime" label="原触发时点"/></el-table>
        </el-tab-pane>
        <el-tab-pane label="保存、审核及打印时机">
          <el-table :data="detail.hook_support" border><el-table-column prop="event" label="原触发时机"/><el-table-column prop="connection" label="开发核验" min-width="240"/><el-table-column prop="historical_reconciliation" label="历史数据对账"/><el-table-column prop="field_acceptance" label="现场验收"/></el-table>
          <el-collapse><el-collapse-item v-for="[key,value] in hooks" :key="key" :title="key"><pre>{{value}}</pre></el-collapse-item></el-collapse><p>这里展示原联动依据。已移植逻辑由业务服务执行；展示配置不等于该联动已开发完成。</p>
        </el-tab-pane>
        <el-tab-pane label="打印（暂缓）"><el-alert title="打印功能暂缓，原版式及配置保留。" type="info" :closable="false"/></el-tab-pane>
      </el-tabs>
    </template>
    <el-dialog v-model="layoutVisible" title="原打印版式核对" width="94%"><p v-for="issue in layout?.proof_issues" :key="issue">填数待补：{{issue}}</p><OriginalLayoutReview v-if="layout" :layout="layout"/></el-dialog>
    <el-dialog v-model="proofVisible" title="原版式填数校样" width="94%"><template v-if="proof"><p>{{proof.record_count}} 行，{{proof.page_count}} 页。{{proof.notes.join(' ')}}</p><p v-if="proof.print_selection">打印{{proof.print_selection.label}}：{{display(proof.print_selection.value)}}；原查询 {{proof.print_selection.input_rows}} 行，本范围 {{proof.print_selection.selected_rows}} 行。</p><p v-if="proof.period">{{proof.period.label}}：{{proof.period.from_inclusive??'全期'}} 至 {{proof.period.until_exclusive??'全期'}}（止日不含）。<span v-if="proof.period.opening_date">期初：{{proof.period.opening_date}}。</span>{{proof.period.source}}</p><iframe :srcdoc="proof.html" sandbox="" title="原版式填数" style="width:100%;height:75vh;border:0"/></template></el-dialog>
  </div>
</template>
<style scoped>.entry-workbench{display:flex;flex-direction:column;gap:12px}.actions{display:flex;flex-wrap:wrap;gap:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>
