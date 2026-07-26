from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for * or /: {} and {}".format(left_type, right_type))

  # Extension 1: operador modulo (%). Conflicto de tipos nuevo:
  # el modulo solo tiene sentido entre enteros; float, string o bool lo invalidan.
  def visitMod(self, ctx: SimpleLangParser.ModContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, IntType) and isinstance(right_type, IntType):
        return IntType()
    else:
        raise TypeError("Unsupported operand types for %: {} and {} (modulo requires int)".format(left_type, right_type))

  # Extension 2: operadores relacionales (< > <= >=). Conflicto de tipos nuevo:
  # solo se comparan valores numericos; el resultado es booleano.
  def visitRelational(self, ctx: SimpleLangParser.RelationalContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return BoolType()
    else:
        raise TypeError("Unsupported operand types for relational {}: {} and {} (requires numeric)".format(ctx.op.text, left_type, right_type))

  # Extension 3: operadores de igualdad (== !=). Conflicto de tipos nuevo:
  # solo se comparan tipos compatibles (mismo tipo, o ambos numericos); da booleano.
  def visitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    both_numeric = isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))
    same_type = type(left_type) == type(right_type)
    if both_numeric or same_type:
        return BoolType()
    else:
        raise TypeError("Cannot compare values of different types with {}: {} and {}".format(ctx.op.text, left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for + or -: {} and {}".format(left_type, right_type))
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
