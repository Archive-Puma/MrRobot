use std::result::Result;

pub type Value<T> = Result<T,Exception>;

#[derive(Debug)]
pub enum Exception {
    ComposerNotFound,
    ComposerNoExtension, ComposerWrongExtension,
    ComposerEmpty,
    ComposerWrongFormat,
    ComposerNoVersion, ComposerWrongVersion,
    ComposerNoSteps,

    StepNoRunAttribute,
    StepWrongWorkName(String),
    StepNoParam(String),
    StepWrongVariable(String),

    NoInternetConnection
}

impl Exception {
    pub fn message(&self) -> String {
        match self {
            Exception::ComposerNotFound        => format!("Cannot read the composer (No such file)"),
            Exception::ComposerNoExtension     => format!("The composer has no extension"),
            Exception::ComposerWrongExtension  => format!("The composer has no YAML extension"),
            Exception::ComposerEmpty           => format!("The composer is empty"),
            Exception::ComposerWrongFormat     => format!("YAML syntax error in composer"),
            Exception::ComposerNoVersion       => format!("Numeric attribute 'version' not specified in composer"),
            Exception::ComposerWrongVersion    => format!("Numeric attribute 'version' has a wrong value (should be: 1)"),
            Exception::ComposerNoSteps         => format!("Vectorial attribute 'steps' not specified in composer"),

            Exception::StepNoRunAttribute      => format!("At least one of the steps does not have the 'run' attribute"),
            Exception::StepWrongWorkName(name) => format!("The work '{}' does not exists", name),
            Exception::StepNoParam(name)       => format!("Parameter '{}' not specified", name),
            Exception::StepWrongVariable(name) => format!("The variable '{}' does not exists", name),
            Exception::NoInternetConnection    => format!("Unable to make the request: Bad url or no Internet connection")
        }
    }
}