from builder import get_available_blocks, build_workflow


async def handle_build_workflow(request):
    # TODO: should handle building process, try/catch and pass request body to build method
    return await build_workflow()


def setup(router):
    router.add_get('/blocks', get_available_blocks)
    router.add_post('/blocks', build_workflow)
