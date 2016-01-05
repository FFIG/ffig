import cppmodel
from cppmodel import TypeKind

def apply_class_annotations(model_class):
    for m in model_class.methods:
        if m.is_pure_virtual:
            model_class.is_abstract = True
        if m.return_type.kind == TypeKind.POINTER and m.return_type.pointee.kind != TypeKind.CHAR_S:
            m.returns_sub_object = True
            m.returns_nullable = True
    
    return model_class
