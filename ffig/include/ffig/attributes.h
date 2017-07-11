// Definitions of attributes used to expose classes and functions through FFIG.

#ifndef FFIG_ATTRIBUTES_H
#define FFIG_ATTRIBUTES_H

#ifdef __clang__
#define FFIG_EXPORT __attribute__((annotate("FFIG:EXPORT")))
#define FFIG_EXPORT_NAME(x) __attribute__((annotate("FFIG:EXPORT"), annotate("FFIG:NAME:"#x)))
#define FFIG_NAME(x) __attribute__((annotate("FFIG:NAME:"#x)))
#define FFIG_PROPERTY __attribute__((annotate("FFIG:PROPERTY")))
#define FFIG_PROPERTY_NAME(x) __attribute__((annotate("FFIG:PROPERTY"), annotate("FFIG:NAME:"#x)))
#else
#define FFIG_EXPORT
#define FFIG_EXPORT_NAME(x)
#define FFIG_NAME(x)
#define FFIG_PROPERTY
#define FFIG_PROPERTY_NAME(x)
#endif

#endif // FFIG_ATTRIBUTES_H

