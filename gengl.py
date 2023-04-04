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

def write_to_file(file, string):
    file.write(string.encode('utf-8'))

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

with open('include/GL/gl.h', 'wb') as file:
    write_to_file(file, f'/* gl.h is a part of glucent\n *\n{license}\n */\n\n')
    write_to_file(file, '''#ifndef __glucent_gl_h_
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
        write_to_file(file, f'GLAPI PFN{proc.upper()}PROC glct_{proc};\n')
        write_to_file(file, f'#define {proc} glct_{proc}\n')

    write_to_file(file, '''
#ifdef __cplusplus
}
#endif // __cplusplus

#endif /* __glucent_gl_h_ */''')

with open('src/gl.c', 'wb') as file:
    write_to_file(file, f'/* gl.c is a part of glucent\n *\n{license}\n */\n\n')
    write_to_file(file, '''#include <GL/gl.h>

#include <stdlib.h>

static void *openGLLib = NULL;

#ifdef _WIN32
#include <windows.h>

typedef PROC(__stdcall *PFNWGLGETPROCADDRESSPROC)(LPCSTR);
static PFNWGLGETPROCADDRESSPROC glctWGLGetProcAddress = NULL;

static int glctLoadOpenGL() {
	openGLLib = LoadLibraryW(L"opengl32.dll");
	if (openGLLib == NULL) {
		return GLCT_ERROR;
	}

	glctWGLGetProcAddress = (PFNWGLGETPROCADDRESSPROC)GetProcAddress(openGLLib, "wglGetProcAddress");
	if (glctWGLGetProcAddress == NULL) {
		return GLCT_ERROR;
	}

	return GLCT_OK;
}

static void glctFreeOpenGL() {
	if (openGLLib) {
		FreeLibrary(openGLLib);
	}
}
#else
#include <dlfcn.h>

#ifndef __APPLE__
typedef void *(*PFNGLXGETPROCADDRESSARB)(const GLubyte *);
PFNGLXGETPROCADDRESSARB glctXGetProcAddress = NULL;
#endif

static int glctLoadOpenGL() {
#ifdef __APPLE__
    openGLLib = dlopen("/System/Library/Frameworks/OpenGL.framework/OpenGL", RTLD_LAZY | RTLD_LOCAL);
#else
	openGLLib = dlopen("libGL.so", RTLD_LAZY | RTLD_LOCAL);
	if (openGLLib == NULL) {
		openGLLib = dlopen("libGL.so.1", RTLD_LAZY | RTLD_LOCAL);
	}
#endif
    if (openGLLib != NULL) {
#ifdef __APPLE__
        return GLCT_OK;
#else
		glctXGetProcAddress = (PFNGLXGETPROCADDRESSARB)dlsym(openGLLib, "glXGetProcAddressARB");
		return glctXGetProcAddress != NULL;
	}
#endif
    return GLCT_ERROR;
}

static void glctFreeOpenGL() {
    if (openGLLib != NULL) {
        dlclose(openGLLib);
    }
}

#endif

static void *glctGetProcAddress(const char *name) {
	if (openGLLib == NULL) {
		return NULL;
	}
	void *address = NULL;
#ifdef _WIN32
	address = (void *)glctWGLGetProcAddress(name);
	if (!address) {
		address = (void *)GetProcAddress(openGLLib, name);
	}
#else
#ifndef __APPLE__
	address = glctXGetProcAddress(name);
#else
    address = dlsym(openGLLib, name);
#endif
#endif

	return address;
}

#define GET_PROC(PROC) (glct_##PROC = glctGetProcAddress(#PROC))

''')

    for proc in procs:
        write_to_file(file, f'PFN{proc.upper()}PROC glct_{proc} = NULL;\n')

    write_to_file(file, '''
int glctInit() {
    if (glctLoadOpenGL() != GLCT_OK) {
        return GLCT_ERROR;
    }

''')

    for proc in procs:
        write_to_file(file, f'\tGET_PROC({proc});\n')

    write_to_file(file, '''
    glctFreeOpenGL();
    return GLCT_OK;
}
''')
