import assert from 'node:assert/strict'
import fs from 'node:fs'
import ts from 'typescript'
const source=fs.readFileSync(new URL('../src/plugins/erp/action-presentation.ts',import.meta.url),'utf8')
const output=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText
const {availableActions,actionTopics}=await import('data:text/javascript;base64,'+Buffer.from(output).toString('base64'))
const action=(key,placement='business',extra={})=>({key,placement,topic:'实际收发',display_title:key,permission:key,detail:true,states:['draft'],...extra})
const actions=[action('receive'),action('reverse','business',{topic:'撤销与更正'}),action('formula','automatic'),action('repair','maintenance'),action('print','deferred')]
assert.deepEqual(availableActions(actions,'draft',{},()=>true).map(a=>a.key),['receive','reverse'])
assert.deepEqual(availableActions(actions,'draft',{},p=>p==='receive').map(a=>a.key),['receive'])
assert.deepEqual(availableActions(actions,'draft',{},()=>true,true).map(a=>a.key),['receive','reverse','formula','repair'])
assert.equal(availableActions(actions,'approved',{},()=>true).length,0)
assert.equal(availableActions(actions,'draft',{transfer_retained:true},()=>true).length,0)
assert.equal(availableActions([action('return','business',{hide_when:['closed']})],'draft',{closed:true},()=>true).length,0)
assert.equal(availableActions([action('query','business',{detail:false})],null,{},()=>true).length,1)
const undo=action('undo','business',{effect_required:'package_pairing'})
assert.equal(availableActions([undo],'draft',{},()=>true).length,0)
assert.equal(availableActions([undo],'draft',{action_effects:{package_pairing:'applied'}},()=>true).length,1)
assert.equal(availableActions([undo],'draft',{action_effects:{package_pairing:'reversed'}},()=>true).length,0)
assert.deepEqual(actionTopics(availableActions(actions,'draft',{},()=>true)).map(g=>[g.title,g.actions.length]),[['实际收发',1],['撤销与更正',1]])
const policies=JSON.parse(fs.readFileSync(new URL('../../backend/plugins/erp_base/button_presentation.json',import.meta.url),'utf8'))
assert.equal(Object.keys(policies).length,1457)
assert.equal(policies['erp_production_sourcedyejobsheet:split_card'].placement,'business')
assert.equal(policies['erp_warehouse_package:request_print'].placement,'deferred')
assert.equal(policies['erp_production_sourcedyejobsheet:phase6_formula'].placement,'maintenance')
console.log('PASS: permissions, states, retained rows, reverse groups, automatic/maintenance reachability, print pause and audited bindings')
