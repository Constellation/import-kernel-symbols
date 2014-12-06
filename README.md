import-kernel-symbols
=====================

A tiny python script to generate headers importing non-exported kernel symbols.

## Motivation

When crafting / testing / experimenting kernel modules, occationally you need to call non-exported kernel symbols.
If you can call non-exported symbols without attaching `EXPORT_SYMBOL` to those symbols, you can try using these functions without modifying / recompiling the kernel.
In addition to this benefit, you can keep your kernel module simple, loadable and external. It's a desirable feature for in-house kernel modules. (When you to upstream it, you simply modify the kernel :))

This python script generates references to the specified non-exported symbols.
It extracts symbol kernel space address from `System.map`, and generates header for easy use.

## Usage

First you need to create the importing header template, `imported.h.in`. This sample is located under `example/` directory.
```c
/*
 * Hello World
 */
#ifndef SAMPLE_H_
#define SAMPLE_H_
#include <linux/mm.h>

IMPORT_SYMBOL_PROLOGUE

IMPORT_SYMBOL(handle_mm_fault);
#endif  /* SAMPLE_H_ */
```

Next, passing it and appropriate `System.map` to `import-kernel-symbols.py` script.
`System.map` is a file containing symbols and addresses in kernel itself. Typically (in Ubuntu case) it is located under `/boot/System.map-$(uname -r)`, or `/lib/modules/$(uname -r)/build/System.map`.
Note that this `System.map` file permission is sometimes set as `-rw-------` with owner `root`. In this case, you need to `sudo` to read `System.map` or change permission of this file.
After hitting the command such as `python import-kernel-symbols.py imported.h.in System.map`, it will dump the generated header. The example is below.

```c
/*
 * Hello World
 */
#ifndef SAMPLE_H_
#define SAMPLE_H_
#include <linux/mm.h>

#define IMPORT_SYMBOL_VALUE_FOR_handle_mm_fault (0xffffffff81198a10UL)
#define IMPORT_SYMBOL(name) \
    static typeof(&name) IMPORTED(name) __attribute__((unused)) = (typeof(&name))IMPORT_SYMBOL_VALUE_FOR_ ## name
#define IMPORTED(name) __i__ ## name


IMPORT_SYMBOL(handle_mm_fault);
#endif  /* SAMPLE_H_ */
```

Since all symbols are resolved by this header correctly, you can call the hidden symbol via special syntax  `IMPORTED(handle_mm_fault)(mm, vma, addr, flags)`.
