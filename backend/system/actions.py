METHODS = {'get': 0, 'post': 1, 'put': 2, 'delete': 3, 'options': 4, 'patch': 5}


def resource_actions(entity, view):
    base = f'/api/system/{entity}/'
    actions = [('list', '查询', 0, base), ('add', '新增', 1, base), ('copy', '复制', 1, base),
               ('detail', '详情', 0, base+'{id}/'), ('edit', '修改', 2, base+'{id}/'),
               ('patch', '局部修改', 5, base+'{id}/'), ('delete', '删除', 3, base+'{id}/')]
    for method in view.get_extra_actions():
        for verb in method.mapping:
            actions.append((method.url_name+'-'+verb, method.__name__, METHODS[verb],
                            base+('{id}/' if method.detail else '')+method.url_path+'/'))
    return actions
