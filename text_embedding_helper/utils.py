import click

@click.group() # 命令的总入口
def main():
    pass

@main.command()
def whiteborder():
    from function_scripts.whiteborder import main_api as whiteborder_api
    
    print('此程序会不断循环，直到您输入\'exit\'退出。')
    while (uinput := input('请输入边框像素大小：')) != 'exit':
        try:
            whiteborder_api(int(uinput))
        except BaseException:
            click.echo('发生错误！最常见的原因是您当前选中的图层不是文字图层，您可以检查一下。')

if __name__ == '__main__':
    main()