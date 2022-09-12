import click

@click.group() # 命令的总入口
def main():
    pass

@main.command()
def whiteborder():
    from function_scripts.whiteborder import main_api as whiteborder_api
    
    print('此程序会不断循环，直到您输入\'exit\'退出。')
    while (uinput := input('请输入边框像素大小')) != 'exit':
        whiteborder_api(int(uinput))