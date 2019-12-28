mod arguments;
pub mod macros;
mod mrerror;

// arguments
pub use arguments::Arguments;
pub use arguments::get_arguments;
// mrerror
pub use mrerror::throw;
pub use mrerror::MrError;
pub use mrerror::Result;