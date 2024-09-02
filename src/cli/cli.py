import click
from typing import Dict, Any
from engine.command_handler import CommandHandler

NEON_PINK = 'bright_magenta'
NEON_BLUE = 'bright_cyan'
NEON_PURPLE = 'bright_blue'
NEON_GREEN = 'bright_green'
NEON_YELLOW = 'bright_yellow'


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


def create_cli(command_handler: CommandHandler):
    @click.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def cli(ctx):
        """HAL-9001 Personal Development CLI"""
        ctx.obj = command_handler
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @cli.command()
    @click.pass_context
    def chat(ctx):
        """Start a chat session"""
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
                result = ctx.obj.handle_command(user_input.lower())
                click.echo(synthwave_style(result, NEON_YELLOW))
            else:
                result = ctx.obj.handle_chat(user_input)
                click.echo(synthwave_style(f"HAL-9001: {result}", NEON_PURPLE))

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

    return cli
