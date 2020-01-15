use crate::{composer::steps, create_work, Variable};

use ssh2::Session;
use std::net::TcpStream;

create_work!(ssh; data, variables => {
    let host: String = steps::get_param("host", data, variables)?;
    let port: String = steps::get_param("port", data, variables).unwrap_or("22".to_string());

    let username: String = steps::get_param("username", data, variables)?;
    let password: String = steps::get_param("password", data, variables)?;

    let dst: String = format!("{}:{}", &host, &port);

    let tcp: TcpStream = TcpStream::connect(&dst).unwrap();
    let mut session = Session::new().unwrap();
    session.set_tcp_stream(tcp);
    session.handshake().unwrap();

    session.userauth_password(&username,&password).unwrap();
    assert!(session.authenticated());

    Ok(Variable::Text("".to_string()))
});