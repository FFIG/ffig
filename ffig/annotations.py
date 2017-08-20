from ffig.clang.cindex import CursorKind, TypeKind


def _set_impl_name(o):
    o.impl_name = o.name
    names = [a for a in o.annotations if a.startswith("FFIG:NAME:")]
    if names:
        o.name = names[-1].replace("FFIG:NAME:", "")


def apply_class_annotations(model_class):
    _set_impl_name(model_class)

    for m in model_class.methods:
        _set_impl_name(m)

        if "FFIG:PROPERTY" in m.annotations:
            m.is_property = True
        if m.is_pure_virtual:
            model_class.is_abstract = True

        if m.return_type.kind == TypeKind.VOID:
            m.returns_void = True
        elif m.return_type.kind in [TypeKind.INT, TypeKind.BOOL, TypeKind.DOUBLE]:
            pass
        elif m.return_type.kind == TypeKind.POINTER and m.return_type.pointee.kind == TypeKind.CHAR_S:
            pass
        elif m.return_type.kind == TypeKind.POINTER:
            m.returns_sub_object = True
            m.returns_nullable = True
        elif m.return_type.kind == TypeKind.LVALUEREFERENCE:
            m.returns_sub_object = True
            m.returns_nullable = False

    return model_class
