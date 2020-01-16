use crate::{composer::steps, create_work, debug, Variable};

use std::fmt::Write;
use sha2::{Sha256, Digest};

create_work!(sha256; data, variables => {
    let msg: String = steps::get_param("encode", data, variables)?;
    debug!("(encode) SHA256: {}", msg);

    let digest = Sha256::digest(msg.as_bytes());

    let mut result = String::with_capacity(&digest.len() * 2);
    for &byte in &digest { let _: Result<(),std::fmt::Error> = write!(&mut result, "{:02x}", byte); }

    Ok(Variable::Text(result))
});