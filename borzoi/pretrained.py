"""Implementation of utilities to load a pretrained Borzoi model in Trix."""

from typing import Callable, Tuple

import haiku as hk
import jax.numpy as jnp

from borzoi.model import BorzoiConfig, build_borzoi_fn_with_head_fn
from enformer.features import FEATURES
from enformer.heads import UNetHead
from enformer.params import download_ckpt
from enformer.tokenizer import NucleotidesKmersTokenizer


def get_pretrained_segment_borzoi_model() -> (
    Tuple[hk.Params, hk.State, Callable, NucleotidesKmersTokenizer, BorzoiConfig]
):
    config = BorzoiConfig()
    tokenizer = NucleotidesKmersTokenizer(
        k_mers=1,
        prepend_bos_token=False,
        prepend_cls_token=False,
        append_eos_token=False,
        tokens_to_ids=None,
    )

    def head_fn() -> hk.Module:
        return UNetHead(
            features=FEATURES,
            embed_dimension=config.embed_dim,
            nucl_per_token=config.dim_divisible_by,
            remove_cls_token=False,
        )

    forward_fn = build_borzoi_fn_with_head_fn(
        config=config,
        head_fn=head_fn,
        embedding_name="embedding",
        name="Borzoi",
        compute_dtype=jnp.float32,
    )

    parameters, state = download_ckpt("segment_borzoi")

    return parameters, state, forward_fn, tokenizer, config
