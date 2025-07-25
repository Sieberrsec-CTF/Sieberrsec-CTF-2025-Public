#define PY_SSIZE_T_CLEAN
#include <python3.9/Python.h>

PyObject *PyInit_mutuple(void);

static PyObject *method_append(PyObject *, PyObject *);

PyMethodDef methods[] = { 
  {
    .ml_name = "append",
    .ml_meth = method_append,
    .ml_flags = METH_VARARGS
  }
};

PyModuleDef definition = {
  .m_name = "mutuple",
  .m_methods = methods,
};

PyObject *PyInit_mutuple() {
  PyModule_Create(&definition);
}

static PyObject *method_append(PyObject *self, PyObject *args) {
  PyTupleObject *the_tuple = NULL;
  PyObject *to_add = NULL;

  if (!PyArg_UnpackTuple(args, "ref", 2, 2, &the_tuple, &to_add)) {
    return NULL;
  }

  if (!PyTuple_Check(the_tuple)) {
    PyErr_SetString(PyExc_TypeError, "first argument must be of type tuple");
    return NULL;
  }

  the_tuple->ob_item[the_tuple->ob_base.ob_size++] = to_add;

  return Py_True;
}
