from app.core import arguments, banner
from app.core.composer  import Composer
from app.core.exception import Elliot

from clint.textui.colored import red

def entrypoint():
    # Get the arguments
    args = arguments.parse()
    # Display the banner
    if not args.no_banner:
        banner.show()
    # Load the composer
    composer = Composer()
    composer.load(args.file)
    # Get the workflow
    workflow = composer.workflow()
    # Execute the workflow
    workflow.run()

if __name__ == "__main__":
    try:
        entrypoint()
    except Elliot as error:
        print(red(f"[!] {error}"))
        
        