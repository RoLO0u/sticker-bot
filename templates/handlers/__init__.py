from templates.handlers import (
    commands, add_sticker, change_sticker,  creating, \
    delete, team, inline, managing, images, start, errors, group
)

routers = (
    commands.router, add_sticker.router, change_sticker.router, creating.router,
    delete.router, team.router, inline.router, managing.router, images.router,
    start.router, errors.router, group.router
)