import webbrowser
import pygame

def check_sequence(key_sequence, target_sequence):
    """Checks if the key sequence matches the target sequence ('exit')."""
    # Keep only the last len(target_sequence) keys
    if len(key_sequence) > len(target_sequence):
        key_sequence.pop(0)
    
    # Check if the sequence matches "exit"
    if key_sequence == target_sequence:
        return True
    return False

# displaying the links to survey and quiz
def display_link():

    # putting text on the screen
    def render_text(text, color, position):

        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)
        return text_surface.get_rect(topleft=position)

    # checking if the mouse is clicked/hovering around hyperlink
    def check_hyperlink(text_rect, link):

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # if mouse is around the link
        if text_rect.collidepoint(mouse_pos):
            if mouse_clicked:
                webbrowser.open(link)  # Open the hyperlink in the web browser
            return True

        return False

    # wrapping text to fit within display
    def wrap_text(text, font, max_width):

        words = text.split(' ')
        lines = []
        current_line = ''

        # adding words into a string until they cannot fit in one line
        for word in words:
            test_line = current_line + word + ' '
            # Check the width of the test_line
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        # adding rest of the remaining words
        if current_line != '':
            lines.append(current_line)

        return lines

    # initializing pygame
    pygame.init()

    # setting values such as colors and size of display
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (0, 100, 255)

    width = 800
    height = 400

    # Set up the display to be full screen
    computer = pygame.display.Info()
    screen_width, screen_height = computer.current_w, computer.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.NOFRAME)
    pygame.display.set_caption("Display Quiz and Survey")

    font = pygame.font.Font('resource/Nanum/NanumGothicCoding-Regular.ttf', 32)

    intro = "영상을 시청해주셔서 감사합니다. 마지막으로 퀴즈와 설문지를 작성해주세요."
    
    intro_lines = wrap_text(intro, font, width)

    links = [("퀴즈", "https://www.google.com"), ("설문지", "https://www.youtube.com")]
    
    yonsei = pygame.image.load('resource/image/Yonsei_Uni_Logo.png')
    yonsei = pygame.transform.smoothscale(yonsei, (100,100))
    yonsei_x = screen_width//2 - yonsei.get_width()/2
    
    running = True

     # entering specific keys in order to close the final screen (on developer end)
    key_sequence = []
    target_sequence = ['c', 'l', 'o', 's', 'e']

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                key_sequence.append(key)
                
                if check_sequence(key_sequence, target_sequence):
                    running = False
        
        screen.fill(WHITE)

        screen.blit(yonsei, (yonsei_x, (screen_height/2)-height/2))

        y_position = (screen_height/2)-height/2 + yonsei.get_height() + 50

        for i, line in enumerate(intro_lines):
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, ((screen_width/2)-width/2, y_position))

            y_position += font.get_height()+2
        
        y_position += font.get_height()

        for text, link in links:

            # Default color is blue
            color = BLUE
            
            # Render the text and get its rectangle
            text_rect = render_text(text, color, ((screen_width/2)-width/2, y_position))
            
            # Check if the hyperlink is hovered or clicked
            if check_hyperlink(text_rect, link):
                # Change color to light blue when hovered
                text_rect = render_text(text, LIGHT_BLUE, ((screen_width/2)-width/2, y_position))
            
            y_position += (2 * font.get_height())

        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    display_link()
