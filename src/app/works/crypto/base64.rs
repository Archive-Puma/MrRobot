use crate::{composer::steps, create_work, debug, raise, Value, Variable};

create_work!(base64; data, variables => {
    let mut result: String = String::new();

    let encode: Value<String> = steps::get_param("encode", data, variables);
    let decode: Value<String> = steps::get_param("decode", data, variables);

    if encode.is_err() && decode.is_err()    { raise!(StepNoParam => "encode")? }
    else if encode.is_ok() && decode.is_ok() { raise!(StepIncompatibleAttr => "encode", "decode")? }

    else if let Ok(msg) = encode { debug!("(encode) base64: {}", msg); result = base64::encode(&msg); }
    else if let Ok(msg) = decode { debug!("(decode) base64: {}", msg); result = String::from_utf8(base64::decode(&msg).unwrap()).unwrap(); }
    
    // FIXME: Handle DecodeError     https://docs.rs/base64/0.11.0/base64/enum.DecodeError.html
    // FIXME: Handle FromUTF-8 Error https://doc.rust-lang.org/std/string/struct.FromUtf8Error.html

    Ok(Variable::Text(result))
});