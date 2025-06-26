#pragma once
#include "ttnn-pybind/pybind_fwd.hpp"

namespace ttnn::operations::experimental::new_op::detail {
namespace py = pybind11;
void bind_experimental_new_operation(py::module& module);

}  // namespace ttnn::operations::experimental::new_op::detail
