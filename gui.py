import wx
from main import movies, recommend_movies


class MyFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title="Movie Recommendation System", size=(900, 600))
        self.Centre()
        self.SetBackgroundColour('#333333')
        self.panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(14, family=wx.DEFAULT, style=0, weight=wx.NORMAL,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)

        # Add text, which is going to be displayed in the GUI
        starting_txt = wx.StaticText(self.panel,
                                     label='Please enter a title of a movie you like and get 10 '
                                           'relevant movie recommendations for it!')
        starting_txt.SetForegroundColour((255, 255, 255))
        starting_txt.SetFont(font)
        my_sizer.Add(starting_txt, 0, wx.ALL | wx.CENTER, 25)

        self.input_message = wx.TextCtrl(self.panel, size=(400, -1))
        my_sizer.Add(self.input_message, 0, wx.ALL | wx.CENTER, 25)

        # Add a button to search for similar movies
        my_btn = wx.Button(self.panel, label='Search recommendations')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 25)

        self.results = wx.StaticText(self.panel, label='')
        self.results.SetForegroundColour((255, 255, 255))
        self.results.SetFont(font)
        my_sizer.Add(self.results, 0, wx.ALL | wx.CENTER)

        self.panel.SetSizer(my_sizer)
        self.Show()

    def on_press(self, event):

        title = self.input_message.GetValue()
        movies['title'] = movies['title'].str.lower()

        if title in movies.values:

            movies['title'] = movies['title'].str.title()
            recommended_movies = recommend_movies(title)
            self.results.SetLabel('Here are 10 recommendations for: '
                                  + title.title() +
                                  '\n\n' + ''.join([str(item) + '\n' for item in recommended_movies]))
            self.input_message.SetLabel('')
            self.input_message.SetFocus()
            self.panel.Layout()
        else:

            self.results.SetLabel('There is no such movie in our database. Please try another title.')
            self.input_message.SetLabel('')
            self.input_message.SetFocus()
            self.panel.Layout()
