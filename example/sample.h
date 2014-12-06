/*
 * Hello World
 */
#ifndef SAMPLE_H_
#define SAMPLE_H_
#include <linux/mm.h>


#define IMPORT_SYMBOL_VALUE_FOR_do_fork (0xffffffff8106ee10UL)
#define IMPORT_SYMBOL_VALUE_FOR_handle_mm_fault (0xffffffff81198a10UL)
#define IMPORT_SYMBOL(name) \
    static typeof(&name) IMPORTED(name) = (typeof(&name))IMPORT_SYMBOL_VALUE_FOR_ ## name
#define IMPORTED(name) __i__ ## name


IMPORT_SYMBOL(handle_mm_fault);
IMPORT_SYMBOL(do_fork);
#endif  /* SAMPLE_H_ */
