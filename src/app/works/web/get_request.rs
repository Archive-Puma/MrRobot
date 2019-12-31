use crate::{composer::steps, create_work, get};

use reqwest::blocking::Response;

create_work!(get_request; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;
    let response: Response = get!(result; reqwest::blocking::get(&url) => NoInternetConnection)?;
    get!(result; response.text() => ComposerEmpty)
});