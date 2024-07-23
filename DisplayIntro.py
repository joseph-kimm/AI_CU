import pygame

# Initialize Pygame
def display_intro():

    # putting text on the screen
    def render_text(text, font, color, position):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)
        return text_surface.get_rect(topleft=position)
    
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


    # Set up the display
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Start Display")

    font = pygame.font.Font('Nanum/NanumGothicCoding-Regular.ttf', 24)

    # Display instructions
    instructions_text_1 = "귀하는 60분 정도 분량의 동영상 1개를 보게 될 것입니다. 해당 동영상은 장애인식개선교육에 대한 것입니다. 동영상을 본 후 연구자가 주관하는 퀴즈와 설문 조사에 참여하도록 요청받을 것입니다."
    instructions_text_2 = "동영상을 시청하실려면 아래의 시작 버튼을 클릭해주세요"

    text_lines_1 = wrap_text(instructions_text_1, font, width-50)
    text_lines_2 = wrap_text(instructions_text_2, font, width-50)

    button_text = "시작"
    button_x = width/2 - font.size(button_text)[0]/2

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button area
                if button_rect.collidepoint(event.pos):
                    return True

        # Fill the screen with white background
        screen.fill(WHITE)

        # Draw line 1
        for i, line in enumerate(text_lines_1):
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, (50, i * font.get_height()+50))

        y_position = (len(text_lines_1) + 1) * font.get_height() + 50

        # Draw line 2
        for i, line in enumerate(text_lines_2):
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, (50, i * font.get_height()+ y_position))

        y_position = y_position + (len(text_lines_2) + 1) * font.get_height()

        # Draw button
        button_rect = render_text(button_text, font, WHITE, (button_x, y_position))

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if button_rect.collidepoint(mouse_pos):
            button_color = LIGHT_BLUE  # Change to lighter color on hover
        else:
            button_color = BLUE  # Default button color

        pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
        render_text(button_text, font, WHITE, button_rect.topleft)

        pygame.display.flip()