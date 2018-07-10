from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from will.plugins.pco import set_list, song_info


class PcoServicesPlugin(WillPlugin):
    @respond_to("(?:do you |find |got |a )?(set list for |!setlist |setlist for |!sunday |songs for |order of service for )(?P<pco_date>.*?(?=(?:\'|\?)|$))")
    def pco_setlist_lookup(self, message , pco_date):
        self.reply("Let me get that for you.")
        setList = set_list.get(pco_date)
        if setList is None:
            self.reply("Sorry I don't have " + setList + "'s set list.")
        # print(setList)
        self.reply(setList)

    @respond_to("(?:what is |show me |what's |a )?(arrangement for |!song )(?P<pco_song>.*?(?=(?:\'|\?)|$))")
    def pco_song_lookup(self, message , pco_song):
        self.reply("Let me get that song for you.")
        attachment = song_info.get(pco_song)
        if attachment is None:
            self.reply("Sorry I don't find " + song + "in services.")
        self.reply("Here you go: ", message=message, attachments=attachment.slack())


# Test your setup by running this file.
# If you add functions in this file please add a test below.


if __name__ == '__main__':
    date = "sunday"
    song_name = "Mighty to Save"
    print("Getting set list for ", date)
    print(set_list.get(date))
    print("Getting song info for ", song_name)
    song = song_info.get(song_name)
    print(song.slack())
