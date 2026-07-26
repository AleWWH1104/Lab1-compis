from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  # Extension 1: modulo (%). Conflicto nuevo: solo entre enteros.
  def enterMod(self, ctx: SimpleLangParser.ModContext):
    pass

  def exitMod(self, ctx: SimpleLangParser.ModContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
      self.errors.append(f"Unsupported operand types for %: {left_type} and {right_type} (modulo requires int)")
    self.types[ctx] = IntType()

  # Extension 2: relacionales (< > <= >=). Conflicto nuevo: solo numericos, da bool.
  def enterRelational(self, ctx: SimpleLangParser.RelationalContext):
    pass

  def exitRelational(self, ctx: SimpleLangParser.RelationalContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for relational {ctx.op.text}: {left_type} and {right_type} (requires numeric)")
    self.types[ctx] = BoolType()

  # Extension 3: igualdad (== !=). Conflicto nuevo: tipos compatibles, da bool.
  def enterEquality(self, ctx: SimpleLangParser.EqualityContext):
    pass

  def exitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    both_numeric = isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))
    same_type = type(left_type) == type(right_type)
    if not (both_numeric or same_type):
      self.errors.append(f"Cannot compare values of different types with {ctx.op.text}: {left_type} and {right_type}")
    self.types[ctx] = BoolType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
