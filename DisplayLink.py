import webbrowser
import pygame

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
        for word in words:
            test_line = current_line + word + ' '
            # Check the width of the test_line
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        if current_line != '':
            lines.append(current_line)
        return lines


    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    width = 800
    height = 400

    # Set up the display
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Display Quiz and Survey")

    font = pygame.font.Font('Nanum/NanumGothicCoding-Regular.ttf', 36)

    intro = "영상을 시청해주셔서 감사합니다. 마지막으로 퀴즈와 설문지를 작성해주세요"
    
    intro_lines = wrap_text(intro, font, width-50)

    links = [("퀴즈", "https://www.google.com"),
             ("설문지", "https://www.youtube.com")]
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)

        # Draw each line of text onto the screen
        for i, line in enumerate(intro_lines):
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, (50, i * font.get_height()+50))
        
        y_position = (len(intro_lines) + 1) * font.get_height() + 50

        for text, link in links:

            # Default color is blue
            color = BLUE
            
            # Render the text and get its rectangle
            text_rect = render_text(text, color, (50, y_position))
            
            # Check if the hyperlink is hovered or clicked
            if check_hyperlink(text_rect, link):
                # Change color to red when hovered
                text_rect = render_text(text, RED, (50, y_position))
            
            y_position += (2 * font.get_height())

        pygame.display.flip()

    pygame.quit()
