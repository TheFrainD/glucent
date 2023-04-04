# gengl.py is a part of glucent
#
# Copyright (c) 2023 Dmytro Zykov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import argparse

extensions = ['arb', 'ext', 'khr', 'ovr', 'nv', 'amd', 'intel', 'mesa']

parser = argparse.ArgumentParser(
    prog='gengl',
    description='glucent OpenGL core profile loader')
parser.add_argument('-e', '-ext', choices=extensions, nargs='+')

args = parser.parse_args()
enabled_extensions = []
if args.e:
    enabled_extensions = args.e
disabled_extensions = list(set(extensions).symmetric_difference(set(enabled_extensions)))

license = ''
with open('LICENSE', 'r') as file:
    for line in file:
        license += f' * {line}'


def matches_extension(proc, ext):
    return proc.endswith(ext.upper())


def is_enabled(proc):
    for ext in disabled_extensions:
        if matches_extension(proc, ext):
            return False
    return True


procs = []
regex = re.compile(r'GLAPI.*APIENTRY\s+(\w+)')
with open('include/GL/glcorearb.h', 'r') as file:
    for line in file:
        m = regex.match(line)
        if not m:
            continue
        proc = m.group(1)
        if is_enabled(proc):
            procs.append(proc)

with open('include/GL/gl.h', 'w') as file:
    file.write(f'/* gl.h is a part of glucent\n *\n{license}\n */\n\n')
    file.write('''#ifndef __glucent_gl_h_
#define __glucent_gl_h_

#include <GL/glcorearb.h>

#ifndef __gl_h_
#define __gl_h_
#endif

#define GLCT_OK 1
#define GLCT_ERROR 0

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

typedef void *(*GLCTgetProcAddress)(const char *name);

int glctInit();\n\n''')

    for proc in procs:
        file.write(f'GLAPI PFN{proc.upper()}PROC glct_{proc};\n')
        file.write(f'#define {proc} glct_{proc}\n')

    file.write('''
#ifdef __cplusplus
}
#endif // __cplusplus

#endif /* __glucent_gl_h_ */''')

with open('src/gl.c', 'w') as file:
    file.write(f'/* gl.c is a part of glucent\n *\n{license}\n */\n\n')
    file.write('''#include <GL/gl.h>

#ifdef __APPLE__
#include <dlfcn.h>

static void *gl_lib;

static int openGl() {
    gl_lib = dlopen("/System/Library/Frameworks/OpenGL.framework/OpenGL", RTLD_LAZY | RTLD_LOCAL);
    if (gl_lib) {
        return GLCT_OK;
    }
    return GLCT_ERROR;
}

static void closeGl() {
    if (gl_lib) {
        dlclose(gl_lib);
    }
}

static void *glctGetProcAddress(const char *name) {
    return dlsym(gl_lib, name);
}
#endif

#ifdef _WIN32
#include <windows.h>

static HMODULE gl_lib;
typedef PROC(__stdcall *PFNWGLGETPROCADDRESSPROC)(LPCSTR);
static PFNWGLGETPROCADDRESSPROC glct_wglGetProcAddress;
#define wglGetProcAddress glct_wglGetProcAddress

static int openGl() {
	gl_lib = LoadLibraryW(L"opengl32.dll");
	if (!gl_lib) {
		return GLCT_ERROR;
	}

	glct_wglGetProcAddress = (PFNWGLGETPROCADDRESSPROC)GetProcAddress(gl_lib, "wglGetProcAddress");
	if (!glct_wglGetProcAddress) {
		return GLCT_ERROR;
	}

	return GLCT_OK;
}

static void closeGl() {
	if (gl_lib) {
		FreeLibrary(gl_lib);
	}
}

static void *glctGetProcAddress(const char *name) {
    void *address = (void *)wglGetProcAddress(name);
	if (!address) {
		return (void *)GetProcAddress(gl_lib, name);
	}
}

#endif // _WIN32


#define GET_PROC(PROC) (glct_##PROC = glctGetProcAddress(#PROC))

''')

    for proc in procs:
        file.write(f'PFN{proc.upper()}PROC glct_{proc};\n')

    file.write('''
int glctInit() {
    if (openGl() != GLCT_OK) {
        return GLCT_ERROR;
    }
    ''')

    for proc in procs:
        file.write(f'\tGET_PROC({proc});\n')

    file.write('''
    closeGl();
    return GLCT_OK;
}
''')
