import cv2
import numpy as np

def C420(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    A = img.astype(np.float32)
    R, G, B = A[...,0], A[...,1], A[...,2]
    H, W = R.shape

    Y  =  0.299 * R + 0.587 * G + 0.114 * B
    Cb = -0.169 * R - 0.331 * G + 0.5   * B + 128
    Cr =  0.5   * R - 0.419 * G - 0.081 * B + 128

    Cb = Cb[0:H:2, 0:W:2]
    Cr = Cr[0:H:2, 0:W:2]

    Cb = cv2.resize(Cb, (W, H), interpolation=cv2.INTER_LINEAR)
    Cr = cv2.resize(Cr, (W, H), interpolation=cv2.INTER_LINEAR)

    R1 = 0.971 * Y - 0.053 * (Cb - 128) + 1.402 * (Cr - 128)
    G1 = 0.971 * Y - 0.396 * (Cb - 128) - 0.714 * (Cr - 128)
    B1 = 0.971 * Y + 1.721 * (Cb - 128) + 0.001 * (Cr - 128)

    comp = np.stack([R1, G1, B1], axis=-1)
    comp = np.clip(comp, 0, 255).astype(np.uint8)

    mse = np.mean((img.astype(np.float32) - comp.astype(np.float32)) ** 2)
    psnr = 10 * np.log10((255 ** 2) / mse) if mse != 0 else float('inf')

    comp = cv2.cvtColor(comp, cv2.COLOR_RGB2BGR)

    return comp, psnr

if __name__ == "__main__":
    img = cv2.imread("./data/input.jpg")

    comp, psnr = C420(img)

    combined = np.hstack((img, comp))

    h, w = combined.shape[:2]
    text = f"Original | PSNR = {psnr:.2f} dB | Reconstructed"

    font = cv2.FONT_HERSHEY_COMPLEX

    (text_w0, text_h0), baseline0 = cv2.getTextSize(text, font, 1, 1)
    font_scale = (w * 0.3) / text_w0

    thickness = max(1, int(h / 300))

    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    x = (w - text_w) // 2
    y = text_h + h // 100

    cv2.putText(
        combined,
        text,
        (x, y),
        font,
        font_scale,
        (0, 0, 0),
        thickness
    )

    cv2.imwrite("./result/result.png", combined)
