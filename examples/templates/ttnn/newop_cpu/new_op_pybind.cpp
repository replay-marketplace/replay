#include "ttnn-pybind/decorators.hpp"

#include "ttnn/operations/experimental/new_op/new_op.hpp"
#include "ttnn/operations/experimental/new_op/new_op_pybind.hpp"

namespace ttnn::operations::experimental::new_op::detail {
namespace py = pybind11;

void bind_experimental_new_operation(py::module& module) {
    auto doc = fmt::format(
        R"doc(
            Operation documentation with api reference and example
        )doc",
        ttnn::experimental::new_op.base_name(),
        ttnn::experimental::new_op.python_fully_qualified_name());
    using OperationType = decltype(ttnn::experimental::new_op);
    bind_registered_operation(
        module,
        ttnn::experimental::new_op,
        doc,
        ttnn::pybind_overload_t{
            [](const OperationType& self,
               const Tensor& input,
               const float probability,
               const float scale,
               const uint32_t seed,
               const std::optional<MemoryConfig>& memory_config,
               const std::optional<Tensor>& output_tensor) { return self(input, probability, scale, seed); },
            py::arg("input_tensor"),
            py::arg("probability"),
            py::arg("scale"),
            py::arg("seed"),
            py::kw_only(),
            py::arg("memory_config") = std::nullopt,
            py::arg("output_tensor") = std::nullopt});
}
}  // namespace ttnn::operations::experimental::new_op::detail
