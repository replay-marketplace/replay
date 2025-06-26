
#include "new_op.hpp"

namespace ttnn::operations::experimental {

Tensor NewOperation::invoke(
    const Tensor& input_tensor, float prob, float scale, uint32_t seed) {

    return Tensor(input_tensor.shape(), input_tensor.tensor_layout());
}

}  // namespace ttnn::operations::experimental
