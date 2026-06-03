import pygame

pygame.init()

class Mesh:

    def __init__(self):

        self.vertices = []

        self.faces = []

class Graphics:

    def __init__(self):

        self.window = None

        self.camera_pitch = 0
        self.camera_yaw = 0

        self.mouse_locked = True

        self.surface = None

        pygame.mixer.init()

        self.sounds = {}

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.mouse_delta_x = 0
        self.mouse_delta_y = 0

        self.camera_pitch = 0
        self.camera_yaw = 0

        self.clock = pygame.time.Clock()

        self.draw_color = (
            255,
            255,
            255
        )

        self.images = {}

        self.width = 800
        self.height = 600

        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = 0

    def limit_fps(self, fps):

        self.clock.tick(fps)

    # ==================================
    # WINDOW
    # ==================================

    def create_window(
        self,
        title,
        width,
        height
    ):

        self.width = width
        self.height = height

        self.window = pygame.display.set_mode(
            (
                width,
                height
            )
        )

        self.window = pygame.display.set_mode(
            (width, height)
        )

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.mouse_locked = True

        pygame.display.set_caption(
            title
        )

        self.surface = self.window

    # ==================================
    # EVENTS
    # ==================================

    def process_events(self):

        if self.mouse_locked:

            self.mouse_delta_x, self.mouse_delta_y = (
                pygame.mouse.get_rel()
            )

        else:

            self.mouse_delta_x = 0
            self.mouse_delta_y = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                    event.type == pygame.KEYDOWN
                    and
                    event.key == pygame.K_ESCAPE
            ):

                self.mouse_locked = (
                    not self.mouse_locked
                )

                pygame.event.set_grab(
                    self.mouse_locked
                )

                pygame.mouse.set_visible(
                    not self.mouse_locked
                )

                if not self.mouse_locked:
                    pygame.mouse.set_pos(
                        (
                            self.width // 2,
                            self.height // 2
                        )
                    )

            if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and
                    not self.mouse_locked
            ):
                self.mouse_locked = True

                pygame.event.set_grab(True)

                pygame.mouse.set_visible(False)

                pygame.mouse.set_pos(
                    (
                        self.width // 2,
                        self.height // 2
                    )
                )

                pygame.mouse.get_rel()

        return True

    def load_obj(self, path):

        mesh = Mesh()

        with open(path, "r") as file:

            for line in file:

                line = line.strip()

                if line.startswith("v "):

                    parts = line.split()

                    x = float(parts[1])
                    y = float(parts[2])
                    z = float(parts[3])

                    mesh.vertices.append(
                        (
                            x,
                            y,
                            z
                        )
                    )

                elif line.startswith("f "):

                    parts = line.split()[1:]

                    face = []

                    for p in parts:
                        idx = int(
                            p.split("/")[0]
                        ) - 1

                        face.append(idx)

                    mesh.faces.append(face)

        return mesh

    def draw_mesh(
            self,
            mesh,
            x,
            y,
            z,
            rot_x,
            rot_y,
            rot_z,
            scale
    ):

        import math

        cos_x = math.cos(rot_x)
        sin_x = math.sin(rot_x)

        cos_y = math.cos(rot_y)
        sin_y = math.sin(rot_y)

        cos_z = math.cos(rot_z)
        sin_z = math.sin(rot_z)

        projected = []
        world_vertices = []

        for vx, vy, vz in mesh.vertices:

            # Scale

            vx *= scale
            vy *= scale
            vz *= scale

            # ==========================
            # X Rotation
            # ==========================

            ry = vy * cos_x - vz * sin_x
            rz = vy * sin_x + vz * cos_x

            vy = ry
            vz = rz

            # ==========================
            # Y Rotation
            # ==========================

            rx = vx * cos_y - vz * sin_y
            rz = vx * sin_y + vz * cos_y

            vx = rx
            vz = rz

            # ==========================
            # Z Rotation
            # ==========================

            rx = vx * cos_z - vy * sin_z
            ry = vx * sin_z + vy * cos_z

            vx = rx
            vy = ry

            # ==========================
            # World Position
            # ==========================

            vx += x
            vy += y
            vz += z

            # ==========================
            # Camera
            # ==========================

            vx -= self.camera_x
            vy -= self.camera_y
            vz -= self.camera_z

            cam_cos_y = math.cos(
                self.camera_yaw
            )

            cam_sin_y = math.sin(
                self.camera_yaw
            )

            rx = (
                    vx * cam_cos_y
                    -
                    vz * cam_sin_y
            )

            rz = (
                    vx * cam_sin_y
                    +
                    vz * cam_cos_y
            )

            vx = rx
            vz = rz

            cam_cos_x = math.cos(
                self.camera_pitch
            )

            cam_sin_x = math.sin(
                self.camera_pitch
            )

            ry = (
                    vy * cam_cos_x
                    -
                    vz * cam_sin_x
            )

            rz = (
                    vy * cam_sin_x
                    +
                    vz * cam_cos_x
            )

            vy = ry
            vz = rz

            # Prevent division by zero

            if vz <= 0.01:
                vz = 0.01

            world_vertices.append(
                (
                    vx,
                    vy,
                    vz
                )
            )

            if rz <= 0.1:
                projected.append(None)

                continue

            projected.append(
                self.project(
                    vx,
                    vy,
                    vz
                )
            )

        # ==========================
        # Draw Faces
        # ==========================

        faces_to_draw = []

        for face in mesh.faces:

            if len(face) < 3:
                continue

            a = face[0]
            b = face[1]
            c = face[2]

            ax, ay, az = world_vertices[a]
            bx, by, bz = world_vertices[b]
            cx, cy, cz = world_vertices[c]

            edge1 = (
                bx - ax,
                by - ay,
                bz - az
            )

            edge2 = (
                cx - ax,
                cy - ay,
                cz - az
            )

            nx = (
                    edge1[1] * edge2[2]
                    -
                    edge1[2] * edge2[1]
            )

            ny = (
                    edge1[2] * edge2[0]
                    -
                    edge1[0] * edge2[2]
            )

            nz = (
                    edge1[0] * edge2[1]
                    -
                    edge1[1] * edge2[0]
            )

            normal_length = (
                                    nx * nx +
                                    ny * ny +
                                    nz * nz
                            ) ** 0.5

            if normal_length == 0:
                continue

            nx /= normal_length
            ny /= normal_length
            nz /= normal_length

            # ==========================
            # CAMERA-FACING CULLING
            # ==========================

            face_x = (
                             ax + bx + cx
                     ) / 3

            face_y = (
                             ay + by + cy
                     ) / 3

            face_z = (
                             az + bz + cz
                     ) / 3

            view_x = -face_x
            view_y = -face_y
            view_z = -face_z

            dot = (
                    nx * view_x +
                    ny * view_y +
                    nz * view_z
            )

            if dot <= 0:
                continue

            points = []

            for vertex_index in face:

                if projected[vertex_index] is None:
                    points = []
                    break

                points.append(
                    projected[vertex_index]
                )

            if len(points) != len(face):
                continue

            # ==========================
            # DEPTH SORTING
            # ==========================

            face_depth = 0

            for vertex_index in face:
                vx, vy, vz = world_vertices[
                    vertex_index
                ]

                face_depth += vz

            face_depth /= len(face)

            # ==========================
            # FLAT LIGHTING
            # ==========================

            brightness = abs(nz)

            brightness = max(
                0.15,
                min(
                    1.0,
                    brightness
                )
            )

            shade = int(
                255 * brightness
            )

            faces_to_draw.append(
                (
                    face_depth,
                    points,
                    (
                        shade,
                        shade,
                        shade
                    )
                )
            )

        faces_to_draw.sort(
            reverse=True
        )

        for depth, points, color in faces_to_draw:
            pygame.draw.polygon(
                self.surface,
                color,
                points
            )

    def mouse_dx(self):

        return self.mouse_delta_x

    def mouse_dy(self):

        return self.mouse_delta_y

    def set_camera_rotation(
            self,
            pitch,
            yaw
    ):

        self.camera_pitch = pitch
        self.camera_yaw = yaw

    def dt(self):

        return self.clock.get_time() / 1000.0

    def mouse_pressed(
            self,
            button
    ):

        buttons = pygame.mouse.get_pressed()

        if button == "left":
            return buttons[0]

        if button == "middle":
            return buttons[1]

        if button == "right":
            return buttons[2]

        return False

    def set_camera(
            self,
            x,
            y,
            z
    ):

        self.camera_x = x
        self.camera_y = y
        self.camera_z = z

    def set_color(
            self,
            r,
            g,
            b
    ):

        self.draw_color = (
            int(r),
            int(g),
            int(b)
        )

    def load_image(
            self,
            path
    ):

        if path not in self.images:
            self.images[path] = pygame.image.load(
                path
            ).convert_alpha()

        return self.images[path]

    def draw_image(
        self,
        path,
        x,
        y,
        width=None,
        height=None
    ):

        image = self.load_image(
            path
        )

        if (
            width is not None
            and
            height is not None
        ):

            image = pygame.transform.scale(
                image,
                (
                    int(width),
                    int(height)
                )
            )

        self.surface.blit(
            image,
            (
                int(x),
                int(y)
            )
        )

    def load_sound(
            self,
            path
    ):

        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(
                path
            )

        return self.sounds[path]

    def play_sound(
            self,
            path
    ):

        sound = self.load_sound(
            path
        )

        sound.play()

    def keep_alive(self):

        running = True

        while running:
            running = self.process_events()

            pygame.time.wait(10)

    # ==================================
    # CLEAR
    # ==================================

    def clear_screen(self):

        self.surface.fill(
            (
                0,
                0,
                0
            )
        )

    def key_pressed(self, key):

        keys = pygame.key.get_pressed()

        mapping = {
            "a": pygame.K_a,
            "d": pygame.K_d,
            "w": pygame.K_w,
            "s": pygame.K_s,
            "space": pygame.K_SPACE,
            "escape": pygame.K_ESCAPE
        }

        if key not in mapping:
            return False

        return keys[mapping[key]]
    
    def mouse_x(self):

        return pygame.mouse.get_pos()[0]

    def mouse_y(self):

        return pygame.mouse.get_pos()[1]
    # ==================================
    # TRIANGLE
    # ==================================

    def draw_triangle(
        self,
        x1,
        y1,
        x2,
        y2,
        x3,
        y3
    ):

        pygame.draw.polygon(
            self.surface,
            self.draw_color,
            [
                (x1, y1),
                (x2, y2),
                (x3, y3)
            ]
        )

    # ==================================
    # RECT
    # ==================================

    def draw_rect(
        self,
        x,
        y,
        width,
        height
    ):

        pygame.draw.rect(
            self.surface,
            self.draw_color,
            (
                x,
                y,
                width,
                height
            )
        )

    def draw_circle(
            self,
            x,
            y,
            radius
    ):

        pygame.draw.circle(
            self.surface,
            self.draw_color,
            (
                int(x),
                int(y)
            ),
            int(radius)
        )
        
    def draw_line(
        self,
        x1,
        y1,
        x2,
        y2
    ):

        pygame.draw.line(
            self.surface,
            self.draw_color,
            (
                int(x1),
                int(y1)
            ),
            (
                int(x2),
                int(y2)
            ),
            2
        )

    def project(
        self,
        x,
        y,
        z
    ):

        fov = 300

        screen_x = (
            x / z
        ) * fov + (
            self.width / 2
        )

        screen_y = (
            y / z
        ) * fov + (
            self.height / 2
        )

        return (
            screen_x,
            screen_y
        )

    def draw_cube(
        self,
        x,
        y,
        z,
        size,
        rotation
    ):

        s = size / 2

        vertices = [

            (-s, -s, -s),
            (s, -s, -s),
            (s, s, -s),
            (-s, s, -s),

            (-s, -s, s),
            (s, -s, s),
            (s, s, s),
            (-s, s, s)

        ]

        edges = [

            (0,1),
            (1,2),
            (2,3),
            (3,0),

            (4,5),
            (5,6),
            (6,7),
            (7,4),

            (0,4),
            (1,5),
            (2,6),
            (3,7)

        ]

        import math

        projected = []
        world_vertices = []

        for vx, vy, vz in vertices:
            rx = (
                    vx * math.cos(rotation)
                    -
                    vz * math.sin(rotation)
            )

            rz = (
                    vx * math.sin(rotation)
                    +
                    vz * math.cos(rotation)
            )
            ry = vy

            rx += x
            ry += y
            rz += z

            rx -= self.camera_x
            ry -= self.camera_y
            rz -= self.camera_z

            # =====================
            # CAMERA YAW
            # =====================

            cam_cos_y = math.cos(
                self.camera_yaw
            )

            cam_sin_y = math.sin(
                self.camera_yaw
            )

            tx = (
                    rx * cam_cos_y
                    -
                    rz * cam_sin_y
            )

            tz = (
                    rx * cam_sin_y
                    +
                    rz * cam_cos_y
            )

            rx = tx
            rz = tz

            # =====================
            # CAMERA PITCH
            # =====================

            cam_cos_x = math.cos(
                self.camera_pitch
            )

            cam_sin_x = math.sin(
                self.camera_pitch
            )

            ty = (
                    ry * cam_cos_x
                    -
                    rz * cam_sin_x
            )

            tz = (
                    ry * cam_sin_x
                    +
                    rz * cam_cos_x
            )

            ry = ty
            rz = tz

            if rz <= 0.01:
                projected.append(None)

                continue

            projected.append(
                self.project(
                    rx,
                    ry,
                    rz
                )
            )

        for a, b in edges:

            if (
                    projected[a] is None
                    or
                    projected[b] is None
            ):
                continue

            x1, y1 = projected[a]
            x2, y2 = projected[b]

            self.draw_line(
                x1,
                y1,
                x2,
                y2
            )

    # ==================================
    # TEXT
    # ==================================

    def draw_text(
        self,
        text,
        x,
        y
    ):

        font = pygame.font.SysFont(
            None,
            30
        )

        surface = font.render(
            str(text),
            True,
            self.draw_color
        )

        self.surface.blit(
            surface,
            (
                x,
                y
            )
        )

    # ==================================
    # PRESENT
    # ==================================

    def present(self):

        pygame.display.flip()