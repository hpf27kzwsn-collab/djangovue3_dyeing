import assert from 'node:assert/strict'
import fs from 'node:fs'
import ts from 'typescript'
import {ref} from 'vue'
const source=fs.readFileSync(new URL('../src/plugins/erp/BusinessPane.vue',import.meta.url),'utf8').match(/<script[^>]*>([\s\S]*?)<\/script>/)[1]
const ast=ts.createSourceFile('BusinessPane.ts',source,ts.ScriptTarget.Latest,true)
const fn=ast.statements.find(node=>ts.isFunctionDeclaration(node)&&node.name.text==='performAction').getText(ast)
const output=ts.transpileModule(fn,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText
const calls=[],row={id:3},operationRow=ref(row),operationOpen=ref(true)
let refreshes=0,fail=false
const globals={props:{entity:'erp_production_sourcedyewprocess'},operationRow,operationOpen,
  api:async(url,options)=>{calls.push({url,options});if(fail)throw Error('业务未通过');return {msg:'操作成功',data:{id:3,approval_stage:'approved'}}},
  showActionResult:()=>{},table:ref({refresh:async()=>{refreshes++}})}
const perform=new Function(...Object.keys(globals),output+';return performAction')(...Object.values(globals))
await perform({key:'approve'},row,{})
assert.equal(operationRow.value.approval_stage,'approved','approval refreshes available actions from saved state')
assert.equal(calls.length,2)
calls.length=0
await perform({key:'delete_shift_record'},row,{})
assert.equal(calls.length,1,'deleted row must not be read again as if it still exists')
assert.equal(operationOpen.value,false);assert.equal(operationRow.value,undefined)
operationRow.value=row;operationOpen.value=true;fail=true
await assert.rejects(perform({key:'approve'},row,{}),/业务未通过/)
assert.equal(operationOpen.value,true);assert.equal(operationRow.value.id,3)
assert.equal(refreshes,2,'failed action must not pretend a saved result')
console.log('PASS: approval state refresh, deleted-row lifecycle, failed action keeps current context')
