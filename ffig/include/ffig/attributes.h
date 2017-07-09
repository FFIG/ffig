// Definitions of attributes used to expose classes and functions through FFIG.

#ifndef FFIG_ATTRIBUTES_H
#define FFIG_ATTRIBUTES_H

#ifdef __clang__
#define FFIG_EXPORT __attribute__((annotate("FFIG:EXPORT")))
#define FFIG_EXPORT_NAME(x) __attribute__((annotate("FFIG:EXPORT"), annotate("FFIG:NAME:"#x)))
#define FFIG_PROPERTY __attribute__((annotate("FFIG:PROPERTY")))
#else
#define FFIG_EXPORT
#define FFIG_EXPORT_NAME(x)
#define FFIG_PROPERTY
#endif

#endif // FFIG_ATTRIBUTES_H

