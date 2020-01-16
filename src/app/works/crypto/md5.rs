use crate::{composer::steps, create_work, debug, raise, Yaml, Value, Variable, Variables, works::web};


create_work!(md5; data, variables => {
    let encode: Value<String> = steps::get_param("encode", data, variables);
    let decode: Value<String> = steps::get_param("decode", data, variables);

    let mut result: String = String::new();

    if encode.is_err() && decode.is_err()    { raise!(StepNoParam => "encode")? }
    else if encode.is_ok() && decode.is_ok() { raise!(StepIncompatibleAttr => "encode", "decode")? }

    else if let Ok(msg) = encode { result = encoder(&msg) }
    else if let Ok(msg) = decode { result = decoder(&msg,data,variables)? }

    Ok(Variable::Text(result))
});


fn encoder(msg: &str) -> String {
    debug!("(encode) MD5: {}", msg);

    let digest: [u8;16] = std::convert::From::from(md5::compute(&msg));
    hex::encode(&digest)
}


fn decoder(msg: &str, data: &Yaml, variables: &Variables) -> Value<String> {
    debug!("(encode) MD5: {}", msg);

    let api: &str = "https://www.nitrxgen.net/md5db/";
    let url: &str = &[api,msg].join("");
    let current_data: Yaml = steps::append_attribute(data, "url", &url);

    let decrypted: Variable = web::request(&current_data, variables)?;

    Ok(decrypted.to_string())
}

/* Documentation:
    - https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
*/