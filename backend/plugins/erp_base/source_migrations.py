"""批量登记原形模型，避免每建一表重复渲染全部关联模型。"""
from django.db.migrations.operations.base import Operation,OperationCategory
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class CreateSourceModels(Operation):
    category=OperationCategory.ADDITION
    serialization_expand_args=['operations']

    def __init__(self,operations):self.operations=operations

    def deconstruct(self):return self.__class__.__qualname__,[],{'operations':self.operations}

    def state_forwards(self,app_label,state):
        # 每个子类登记同类操作；先统一更新状态，再由数据库操作渲染一次。
        state.is_delayed=True
        state.clear_delayed_apps_cache()
        for operation in self.operations:operation.state_forwards(app_label,state)

    def database_forwards(self,app_label,schema_editor,from_state,to_state):
        for operation in self.operations:
            operation.database_forwards(app_label,schema_editor,from_state,to_state)

    def database_backwards(self,app_label,schema_editor,from_state,to_state):
        for operation in reversed(self.operations):
            operation.database_backwards(app_label,schema_editor,from_state,to_state)

    def describe(self):return 'Create '+str(len(self.operations))+' complete source models'


class AddSourceIndexes(CreateSourceModels):
    def describe(self):return 'Add '+str(len(self.operations))+' original key indexes'


class RemoveSourceFields(CreateSourceModels):
    """批量删除互不依赖的可空来源列；保留标准RemoveField的数据库行为。"""
    category=OperationCategory.REMOVAL

    def describe(self):return 'Remove '+str(len(self.operations))+' redundant source fields'


class AddSourceConstraints(CreateSourceModels):
    def describe(self):return 'Add '+str(len(self.operations))+' source row identities'


class AddSourceRelations(CreateSourceModels):
    def database_forwards(self,app_label,schema_editor,from_state,to_state):
        for operation in self.operations:
            model=to_state.apps.get_model(app_label,operation.model_name)
            field=model._meta.get_field(operation.name)
            if operation.allow_migrate_model(schema_editor.connection.alias,model):
                if schema_editor.connection.vendor=='sqlite':
                    # 本组只含无默认值的可空 FK，SQLite 可直接添加带引用的空列。
                    BaseDatabaseSchemaEditor.add_field(schema_editor,model,field)
                else:schema_editor.add_field(model,field)

    def database_backwards(self,app_label,schema_editor,from_state,to_state):
        # 回退采用逐字段中间状态，确保同一表有多个 FK 时保留其他列。
        states=[];current=to_state
        for operation in self.operations:
            states.append(current);current=current.clone()
            operation.state_forwards(app_label,current)
        for operation,previous in reversed(list(zip(self.operations,states))):
            operation.database_backwards(app_label,schema_editor,current,previous)
            current=previous

    def describe(self):return 'Add '+str(len(self.operations))+' nullable source relations'


class AlterSourceFormFields(CreateSourceModels):
    """仅修改 blank/editable 的表单状态，数据库列不变。"""
    category=OperationCategory.ALTERATION

    def database_forwards(self,app_label,schema_editor,from_state,to_state):pass

    def database_backwards(self,app_label,schema_editor,from_state,to_state):pass

    def describe(self):return 'Update '+str(len(self.operations))+' source form fields'
