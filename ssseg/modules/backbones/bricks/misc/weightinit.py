'''
Function:
    weight initialize
Author:
    Zhenchao Jin
'''
import math
import torch
import warnings


'''reference: https://people.sc.fsu.edu/~jburkardt/presentations/truncated_normal.pdf'''
def _no_grad_trunc_normal_(tensor, mean, std, a, b):
    '''computes standard normal cumulative distribution function'''
    def norm_cdf(x):
        return (1. + math.erf(x / math.sqrt(2.))) / 2.
    if (mean < a - 2 * std) or (mean > b + 2 * std):
        warnings.warn('mean is more than 2 std from [a, b] in nn.init.trunc_normal_. The distribution of values may be incorrect.', stacklevel=2)
    # values are generated by using a truncated uniform distribution and then using the inverse CDF for the normal distribution. 
    with torch.no_grad():
        # get upper and lower cdf values
        lower_bound = norm_cdf((a - mean) / std)
        upper_bound = norm_cdf((b - mean) / std)
        # uniformly fill tensor with values from [l, u], then translate to [2l-1, 2u-1].
        tensor.uniform_(2 * lower_bound - 1, 2 * upper_bound - 1)
        # use inverse cdf transform for normal distribution to get truncated standard normal
        tensor.erfinv_()
        # transform to proper mean, std
        tensor.mul_(std * math.sqrt(2.))
        tensor.add_(mean)
        # clamp to ensure it's in the proper range
        tensor.clamp_(min=a, max=b)
        return tensor


'''
Fills the input Tensor with values drawn from a truncated normal distribution. 
The values are effectively drawn from the normal distribution :math:`\mathcal{N}(\text{mean}, \text{std}^2)` with values outside :math:`[a, b]` redrawn until they are within the bounds. 
The method used for generating the random values works best when :math:`a \leq \text{mean} \leq b`.
Args:
    tensor (``torch.Tensor``): an n-dimensional `torch.Tensor`
    mean (float): the mean of the normal distribution
    std (float): the standard deviation of the normal distribution
    a (float): the minimum cutoff value
    b (float): the maximum cutoff value
'''
def truncnormal(tensor, mean=0., std=1., a=-2., b=2.):
    return _no_grad_trunc_normal_(tensor, mean, std, a, b)