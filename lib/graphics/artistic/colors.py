def lerp_colors(colors, t):
    num_segments = len(colors) - 1
    segment = int(t * num_segments)
    print(num_segments)

    t_segment = (t * num_segments) - segment
    print(segment+1)
    color1 = colors[segment]
    color2 = colors[segment + 1]

    r = color1[0] * (1 - t_segment) + color2[0] * t_segment
    g = color1[1] * (1 - t_segment) + color2[1] * t_segment
    b = color1[2] * (1 - t_segment) + color2[2] * t_segment

    return (r, g, b)