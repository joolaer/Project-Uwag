from settings import *

CHARACTER_DATA = {
    'mary': {
        'stats': {
          'love': 100,
          'lust': 50,
          'manipulation': 0,
          'desperation': 0,
          'corruption': 0,
          'morals': 100,  
        },
        'idle': {
            'right' : [
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'right', '0.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'right', '1.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'right', '2.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'right', '3.png'))
            ],
            'left' : [
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'left', '0.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'left', '1.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'left', '2.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'idle', 'left', '3.png'))
            ]
        },
        'face': {
            'normal': [
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '0.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '1.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '2.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '3.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '4.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '5.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '6.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '7.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '8.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '9.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '10.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '11.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '12.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '13.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '14.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '15.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'normal', '16.png')),
            ],
            'sus': [
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '0.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '1.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '2.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '3.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '4.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '5.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '6.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '7.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '8.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '9.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '10.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '11.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '12.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '13.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '14.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '15.png')),
                pygame.image.load(join('media', 'animation', 'mary', 'face', 'sus', '16.png')),
            ]
        }
    }
}