#pragma once

#include "ttnn/decorators.hpp"
#include "ttnn/tensor/tensor.hpp"

namespace ttnn::operations::experimental {

struct NewOperation {
    static Tensor invoke(
        const Tensor& input_tensor, float prob, float scale, uint32_t seed);
};

}  // namespace ttnn::operations::experimental
namespace ttnn::experimental {
constexpr auto new_op =
    ttnn::register_operation<"ttnn::experimental::new_op", ttnn::operations::experimental::NewOperation>();
}  // namespace ttnn::experimental
