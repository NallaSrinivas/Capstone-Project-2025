import sys

class custom_exception(Exception):
    def __init__(self, error_msg , error_details:sys):
        self.error_msg = error_msg
        _, _, exc_tb = error_details.exc_info()
        print(exc_tb)

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "error occured in python script name [{0}] line number [{1}] error message [{2}]".format(self.filename , self.lineno, str(self.error_msg))



if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        raise custom_exception(e, sys)
        # print(e)