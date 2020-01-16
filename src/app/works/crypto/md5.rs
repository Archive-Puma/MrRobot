use crate::{composer::steps, create_work, debug, Variable};


create_work!(md5; data, variables => {
    let msg: String = steps::get_param("encode", data, variables)?;
    debug!("(encode) MD5: {}", msg);

    let digest: [u8;16] = std::convert::From::from(md5::compute(&msg));
    let hex: String = hex::encode(&digest);

    Ok(Variable::Text(hex))
});