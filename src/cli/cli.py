import click
from typing import Dict, Any
from engine.command_handler import CommandHandler
import logging
from database.models.model import ENTITY_TYPES
from datetime import datetime, date, time
from pydantic import BaseModel


NEON_PINK = 'bright_magenta'
NEON_BLUE = 'bright_cyan'
NEON_PURPLE = 'bright_blue'
NEON_GREEN = 'bright_green'
NEON_YELLOW = 'bright_yellow'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SynthwaveGroup(click.Group):
    def format_help(self, ctx, formatter):
        formatter.write(synthwave_style(
            self.get_short_help_str() + "\n", NEON_BLUE))
        formatter.write(synthwave_style(
            "Usage: " + ctx.command_path + " [OPTIONS] COMMAND [ARGS]...\n", NEON_GREEN))
        self.format_options(ctx, formatter)
        self.format_commands(ctx, formatter)

    def format_options(self, ctx, formatter):
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section(synthwave_style("Options:", NEON_GREEN)):
                formatter.write_dl([(synthwave_style(opt[0], NEON_PURPLE), synthwave_style(
                    opt[1], NEON_BLUE)) for opt in opts])


def synthwave_style(text, color):
    return click.style(text, fg=color, bold=True)


def create_cli():
    @click.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def cli(ctx):
        """HAL-9001 Personal Development CLI"""
        ctx.obj = CommandHandler()
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @cli.command()
    @click.pass_context
    def chat(ctx):
        """Start a chat session"""
        command_handler = ctx.obj

        click.echo(synthwave_style("Starting chat session...", NEON_BLUE))
        click.echo(synthwave_style(
            "Type 'exit' to end the session, or 'help' for available commands.", NEON_YELLOW))
        while True:
            user_input = click.prompt(synthwave_style(
                "You", NEON_GREEN), prompt_suffix=": ")
            if user_input.lower() == 'exit':
                click.echo(synthwave_style(
                    "Ending chat session...", NEON_BLUE))
                break
            elif user_input.lower() in ['history', 'clear', 'help']:
                result = command_handler.handle_command(user_input.lower())
                click.echo(synthwave_style(result, NEON_YELLOW))
            else:
                result = command_handler.handle_chat(user_input)
                click.echo(synthwave_style("HAL-9001:", NEON_PURPLE))
                for line in result.split('\n'):
                    click.echo(synthwave_style(line, NEON_PINK))

    @cli.command()
    @click.pass_context
    def history(ctx):
        """Show conversation history"""
        result = ctx.obj.handle_command('history')
        click.echo(synthwave_style(result, NEON_YELLOW))

    @cli.command()
    @click.pass_context
    def clear(ctx):
        """Clear conversation history"""
        result = ctx.obj.handle_command('clear')
        click.echo(synthwave_style(result, NEON_YELLOW))

    def create_entity_commands(entity_type: str, entity_class):
        @cli.group(name=entity_type)
        def entity_group():
            pass

        @entity_group.command('add')
        @click.pass_context
        def add(ctx):
            """Add a new entity"""
            data = {}
            for field, field_info in entity_class.__fields__.items():
                if field not in ['id', 'created_at', 'updated_at']:
                    if isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseModel):
                        continue  # Skip nested models for now
                    if field_info.annotation == date:
                        value = click.prompt(synthwave_style(
                            f"{field.capitalize()}", NEON_GREEN), type=click.DateTime(formats=["%Y-%m-%d"]))
                        data[field] = value.date()
                    elif field_info.annotation == time:
                        value = click.prompt(synthwave_style(
                            f"{field.capitalize()}", NEON_GREEN), type=click.DateTime(formats=["%H:%M"]))
                        data[field] = value.time()
                    elif field_info.annotation == int:
                        data[field] = click.prompt(synthwave_style(
                            f"{field.capitalize()}", NEON_GREEN), type=int)
                    else:
                        data[field] = click.prompt(synthwave_style(
                            f"{field.capitalize()}", NEON_GREEN))

            notes = click.prompt(synthwave_style(
                "Notes (optional)", NEON_GREEN), default='')

            result = ctx.obj.handle_command(
                f'create_{entity_type}', data=data, notes=notes)
            click.echo(synthwave_style(result, NEON_YELLOW))

        @entity_group.command('list')
        @click.pass_context
        def list_entities(ctx):
            """List all entities"""
            result = ctx.obj.handle_command(f'list_{entity_type}')
            click.echo(synthwave_style(result, NEON_YELLOW))

        @entity_group.command('get')
        @click.pass_context
        @click.argument('entity_id')
        def get(ctx, entity_id):
            """Get entity details"""
            result = ctx.obj.handle_command(
                f'get_{entity_type}', entity_id=entity_id)
            click.echo(synthwave_style(result, NEON_YELLOW))

        @entity_group.command('update')
        @click.pass_context
        @click.argument('entity_id')
        def update(ctx, entity_id):
            """Update entity details"""
            data = {}
            entity = ctx.obj.handle_command(
                f'get_{entity_type}', entity_id=entity_id)
            for field, field_info in entity_class.__fields__.items():
                if field not in ['id', 'created_at', 'updated_at']:
                    if isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseModel):
                        continue  # Skip nested models for now
                    current_value = getattr(entity, field, None)
                    if field_info.annotation == date:
                        value = click.prompt(synthwave_style(f"{field.capitalize()}", NEON_GREEN),
                                             type=click.DateTime(
                                                 formats=["%Y-%m-%d"]),
                                             default=current_value.isoformat() if current_value else None)
                        if value:
                            data[field] = value.date()
                    elif field_info.annotation == time:
                        value = click.prompt(synthwave_style(f"{field.capitalize()}", NEON_GREEN),
                                             type=click.DateTime(
                                                 formats=["%H:%M"]),
                                             default=current_value.isoformat() if current_value else None)
                        if value:
                            data[field] = value.time()
                    elif field_info.annotation == int:
                        value = click.prompt(synthwave_style(f"{field.capitalize()}", NEON_GREEN),
                                             type=int,
                                             default=current_value)
                        if value != current_value:
                            data[field] = value
                    else:
                        value = click.prompt(synthwave_style(f"{field.capitalize()}", NEON_GREEN),
                                             default=str(current_value) if current_value is not None else None)
                        if value != str(current_value):
                            data[field] = value

            notes = click.prompt(synthwave_style(
                "Notes (optional)", NEON_GREEN), default='')

            result = ctx.obj.handle_command(
                f'update_{entity_type}', entity_id=entity_id, data=data, notes=notes)
            click.echo(synthwave_style(result, NEON_YELLOW))

        @entity_group.command('delete')
        @click.pass_context
        @click.argument('entity_id')
        @click.confirmation_option(prompt='Are you sure you want to delete this entity?')
        def delete(ctx, entity_id):
            """Delete an entity"""
            result = ctx.obj.handle_command(
                f'delete_{entity_type}', entity_id=entity_id)
            click.echo(synthwave_style(result, NEON_YELLOW))

    for entity_type, entity_class in ENTITY_TYPES.items():
        create_entity_commands(entity_type, entity_class)

    return cli


if __name__ == '__main__':
    cli = create_cli()
    cli()
