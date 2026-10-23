import assert from 'node:assert/strict'
import fs from 'node:fs'
import ts from 'typescript'
import * as vue from 'vue'

const script=fs.readFileSync(new URL('../src/plugins/erp/OrderPriceChooser.vue',import.meta.url),'utf8').match(/<script[^>]*>([\s\S]*?)<\/script>/)[1].replace(/^import .*$/gm,'')
const output=ts.transpileModule(script,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText
const scope=vue.effectScope()
await scope.run(async()=>{
  const props=vue.reactive({row:{id:1,old_prod_id:'P',old_unit:'KG',old_order_qty:'10'},order:{id:2,old_customer_id:'C'}})
  const emissions=[],requests=[],messages=[]
  const globals={computed:vue.computed,reactive:vue.reactive,ref:vue.ref,watch:vue.watch,defineProps:()=>props,defineEmits:()=>((...args)=>emissions.push(args)),defineExpose:()=>{},
    ElMessage:{info:text=>messages.push(text)},api:async(url,options)=>{requests.push({url,...options});return {data:{price:'3.25',amount:'32.50',adoption:{quantity_basis:'订单KG'}}}}}
  const state=new Function(...Object.keys(globals),output+';return {choice,choose,prepare,unchanged,payload,preview}')( ...Object.values(globals))
  state.choice.yarn_category='客户来纱';await vue.nextTick()
  state.choose({quote_id:3,quote_head_id:4,yarn_category:'客户来纱',price_unit:1});await vue.nextTick()
  assert.equal(emissions.at(-1)[1].quote_id,3)
  assert.equal(requests.length,0,'choosing does not require a preview request')
  assert.equal((await state.prepare()).quote_id,3,'save prepares the chosen quote directly')
  assert.equal(requests.at(-1).data.pricing.quote_head_id,4)
  state.unchanged();assert.equal(await state.prepare(),null,'cancel cannot silently reapply the prior selection')
  state.choose({quote_id:5,quote_head_id:4,yarn_category:'客户来纱',price_unit:1});await vue.nextTick()
  assert.equal((await state.prepare()).quote_id,5)
  state.choice.yarn_category='本厂采购';await vue.nextTick()
  assert.equal(emissions.at(-1)[1],null,'changing yarn supply invalidates the chosen quote')
  assert.equal(await state.prepare(),null)
  state.choice.mode='manual';state.choice.manual_price=0;await vue.nextTick()
  assert.equal((await state.prepare()).manual_price,0,'zero is a real manual price')
  state.choice.manual_price='-2.50';await vue.nextTick()
  assert.equal((await state.prepare()).manual_price,'-2.50','negative data is passed to the pricing service without rewriting')
  state.choice.manual_price='';await vue.nextTick()
  assert.equal((await state.prepare()).manual_price,null,'empty manual price stays NULL')
  props.row.old_prod_id='OTHER';await vue.nextTick()
  assert.equal(emissions.at(-1)[1],null,'material change requires a new pricing decision')
})
scope.stop()
console.log('PASS: direct save, cancellation, new selection, supply/material change, zero/negative/NULL manual pricing')
