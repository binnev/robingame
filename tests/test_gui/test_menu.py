from unittest.mock import MagicMock, patch

from robingame.gui import Menu, Button


@patch("robingame.gui.menu.pygame.mouse.get_pressed")
@patch("robingame.utils.pygame.mouse.get_pos")
def test_update_buttons(mock_mouse_pos, mock_mouse_buttons, font_init):
    mock_on_press = MagicMock()
    mock_on_release = MagicMock()
    mock_on_focus = MagicMock()
    mock_on_unfocus = MagicMock()

    menu = Menu()
    button = Button(
        x=0,
        y=0,
        width=10,
        height=10,
        on_press=mock_on_press,
        on_release=mock_on_release,
        on_focus=mock_on_focus,
        on_unfocus=mock_on_unfocus,
    )
    menu.buttons.add(button)

    # nothing has happened yet
    mock_mouse_pos.return_value = (69, 420)
    mock_mouse_buttons.return_value = (0, 0, 0)
    menu.update()
    assert mock_on_press.call_count == 0
    assert mock_on_release.call_count == 0
    assert mock_on_focus.call_count == 0
    assert mock_on_unfocus.call_count == 0

    # mouse hovers over button
    mock_mouse_pos.return_value = button.rect.center
    menu.update()
    assert mock_on_press.call_count == 0
    assert mock_on_release.call_count == 0
    assert mock_on_focus.call_count == 1
    assert mock_on_unfocus.call_count == 0

    # mouse clicks
    mock_mouse_buttons.return_value = (1, 0, 0)
    menu.update()
    assert mock_on_press.call_count == 1
    assert mock_on_release.call_count == 0
    assert mock_on_focus.call_count == 1
    assert mock_on_unfocus.call_count == 0

    # time passes, no new mouse click
    # (mouse button is still down but it shouldn't register as another click)
    menu.update()
    assert mock_on_press.call_count == 1
    assert mock_on_release.call_count == 0
    assert mock_on_focus.call_count == 1
    assert mock_on_unfocus.call_count == 0

    # mouse unclicks
    mock_mouse_buttons.return_value = (0, 0, 0)
    menu.update()
    assert mock_on_press.call_count == 1
    assert mock_on_release.call_count == 1
    assert mock_on_focus.call_count == 1
    assert mock_on_unfocus.call_count == 0

    # mouse moves away
    mock_mouse_pos.return_value = (69, 420)
    menu.update()
    assert mock_on_press.call_count == 1
    assert mock_on_release.call_count == 1
    assert mock_on_focus.call_count == 1
    assert mock_on_unfocus.call_count == 1
