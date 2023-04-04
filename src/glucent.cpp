//#include <glucent/glucent.h>
//
//#include <string>
//
//#include <OpenGL/CGLTypes.h>
//#include <dlfcn.h>
//
//static void *libgl;
//
//static int LoadOpenGL() {
//    libgl = dlopen("/System/Library/Frameworks/OpenGL.framework/OpenGL", RTLD_LAZY | RTLD_LOCAL);
//    if (libgl) return 1;
//    return 0;
//}
//
//static void CloseOpenGL() {
//    if (libgl) {
//        dlclose(libgl);
//        libgl = nullptr;
//    }
//}
//
//static void *LoadFunction(const std::string& name) {
//    return dlsym(libgl, name.c_str());
//}
//
//namespace glucent
//{
//    std::function<void((GLint x, GLint y, GLsizei width, GLsizei height))> glViewport;
//    std::function<void((GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha))> glClearColor;
//    std::function<void(GLbitfield mask)> glClear;
//    std::function<const GLubyte *(GLenum name)> glGetString;
//
//    int Init() {
//        if (!LoadOpenGL()) {
//            return 0;
//        }
//
//        if (!(glViewport = (void(*)(GLint, GLint, GLsizei, GLsizei))LoadFunction("glViewport"))) {
//            return 0;
//        }
//
//        if (!(glClearColor = (void(*)(GLclampf, GLclampf, GLclampf, GLclampf))LoadFunction("glClearColor"))) {
//            return 0;
//        }
//
//        if (!(glClear = (void(*)(GLbitfield))LoadFunction("glClear"))) {
//            return 0;
//        }
//
//        if (!(glGetString = (const GLubyte *(*)(GLenum))LoadFunction("glGetString"))) {
//            return 0;
//        }
//
//        CloseOpenGL();
//
//        return 1;
//    }
//
//}
