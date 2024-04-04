import math


class RCCBeam:
    """
    Class for designing RCC beams based on IS 456.
    Attributes:
        fck (float): Characteristic compressive strength of concrete (MPa).
        fy (float): Yield strength of steel (MPa).
        b (float): Width of the beam section (mm).
        h (float): Overall depth of the beam section (mm).
        d (float): Effective depth of the beam section (mm).
        cover (float): Effective cover to reinforcement (mm).
        fy (float): Yield strength of steel (MPa).
        Mu (float): Target moment to be resisted by the beam (kN m).
    """

    def __init__(self, fck, fy, b=300, h=500, Mu=100):
        self.fck = fck
        self.fy = fy
        self.b = b
        self.h = h
        self.cover = 25  # cover can be changed later
        self.d = self.h - self.cover  # Effective depth calculated later
        self.Mu = Mu
        self.Ast = None
        self.Es = 2 * 10**5
        self.xu_lim = self.calculate_xulim()
        self.Mu_lim = self.calculate_Mulim()

    def set_cover(self, cover):
        """
        Sets the cover to reinforcement and updates the effective depth.
        """
        self.cover = cover
        self.d = self.h - self.cover

    def calculate_xulim(self):
        xu_lim = (0.0035 * self.d) / (0.0055 + 0.87 * self.fy / self.Es)
        return xu_lim

    def calculate_Mulim(self):
        mu_lim = (
            0.36
            * self.fck
            * self.b
            * self.xu_lim
            * (self.d - 0.416 * self.xu_lim)
            * 10**-6
        )
        return round(mu_lim, 2)

    def calculate_MOR(self, n=3, dia=16):
        """
        Calculates the moment of resistance (M) of the beam section based on area of reinforcement provided.
        Returns:
            float: Moment of resistance of the beam section (kNm).
        """
        Ast = n * math.pi * (dia**2) / 4
        xu = 0.87 * self.fy * Ast / (0.36 * self.fck * self.b)
        if xu < self.xu_lim:
            MoR = (
                0.87
                * self.fy
                * Ast
                * self.d
                * (1 - Ast * self.fy / (self.b * self.d * self.fck))
                * 10**-6
            )
            return round(MoR, 2)
        else:
            raise NotImplementedError(
                "Moment of resistance calculation for over-reinforced section not implemented."
            )

    def calculate_Ast_req(self):
        """
        Calculates the required area of steel (As) based on the design moment.
        Returns:
            float: Required area of steel (mm^2).
        """
        if self.Mu > self.Mu_lim:
            raise NotImplementedError(
                "This is over-reinforced section, which is not implemented yet."
            )
        alpha = (self.Mu * 10**6) / (self.b * self.d**2)
        p = (1 - math.sqrt(1 - 4.598 * alpha / self.fck)) * self.fck / (2 * self.fy)
        Ast = p * self.b * self.d
        self.Ast = Ast
        return round(Ast, 2)


# Example usage
beam = RCCBeam(fck=20, fy=415, b=250, h=500, Mu=120)
print(beam.Mu_lim)
print(beam.calculate_Ast_req())
print("hello")
