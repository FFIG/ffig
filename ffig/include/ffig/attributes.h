// Definitions of attributes used to expose classes and functions through FFIG.

#ifndef FFIG_ATTRIBUTES_H
#define FFIG_ATTRIBUTES_H

#ifdef __clang__
#define FFIG_EXPORT __attribute__((annotate("GENERATE_C_API")))
#else
#define FFIG_EXPORT
#endif

#endif // FFIG_ATTRIBUTES_H

