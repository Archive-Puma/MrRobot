use std::result::Result;

pub type Value<T> = Result<T,Exception>;

#[derive(Debug)]
pub enum Exception {
    ComposerNotFound,
    ComposerNoExtension, ComposerWrongExtension,
    ComposerEmpty,
    ComposerWrongFormat,
    ComposerNoVersion, ComposerWrongVersion,
    ComposerNoSteps
}

impl Exception {
    pub fn message(&self) -> &'static str {
        match *self {
            Exception::ComposerNotFound        => "Cannot read the composer (No such file)",
            Exception::ComposerNoExtension     => "The composer has no extension",
            Exception::ComposerWrongExtension  => "The composer has no YAML extension",
            Exception::ComposerEmpty           => "The composer is empty",
            Exception::ComposerWrongFormat     => "YAML syntax error in composer",
            Exception::ComposerNoVersion       => "Numeric attribute 'version' not specified in composer",
            Exception::ComposerWrongVersion    => "Numeric attribute 'version' has a wrong value (should be: 1)",
            Exception::ComposerNoSteps         => "Vectorial attribute 'steps' not specified in composer"
        }
    }
}
