

class Board(models.Model):
    topic = models.CharField(max_length=100)
    description = models.TextField()
    # owner = models.ForeignKey('auth.User', related_name='board_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('auth.User', blank=True, related_name='available_board_set')

    class Meta:
        ordering = ['created']


class Section(models.Model):
    board = models.ForeignKey(Board, related_name='section_set', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField()


class Card(models.Model):
    section = models.ForeignKey(Board, related_name='card_set', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    performer = models.ForeignKey('auth.User', null=True, blank=True, related_name='performing_card_set',
                                  on_delete=models.SET_NULL)
