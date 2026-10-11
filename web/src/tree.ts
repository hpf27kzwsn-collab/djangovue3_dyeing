export function toTree(rows:any[],pk='id',parent='parent') {
  const nodes=new Map(rows.map(row=>[row[pk],{...row,children:[]}]))
  const roots:any[]=[]
  for(const row of rows){const node=nodes.get(row[pk])!;const parentNode=nodes.get(row[parent]);if(parentNode) parentNode.children.push(node as never);else roots.push(node)}
  return roots
}
